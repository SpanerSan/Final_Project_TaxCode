"""Evaluate retrieval on the fixed checkpoint questions."""

import argparse
import json
from pathlib import Path

from main import ROOT, load_corpus
from rag import OpenAI, VectorIndex

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--llm", action="store_true", help="Evaluate OpenAI retrieval and print answers for manual review")
args = parser.parse_args()

_, passages = load_corpus()
try:
    provider = OpenAI.from_environment(ROOT / ".env") if args.llm else None
    index = VectorIndex(passages, provider)
    cases = json.loads(Path(ROOT / "evaluation" / "questions.json").read_text(encoding="utf-8"))
    hits = evaluated = 0
    for case in cases:
        question = case["question"]
        expected = (case["article"], case["point"])
        ranked = index.search(question)
        actual = (ranked[0].article, ranked[0].point) if ranked else (None, None)
        if expected[0] is not None:
            hits += actual == expected
            evaluated += 1
            status = "PASS" if actual == expected else "MISS"
        else:
            status = "NO MATCH" if not ranked else "REVIEW"
        print(f"{status}: {question} | expected={expected} | top={actual}")
        if provider:
            answer, sources = provider.answer(question, ranked)
            print("  ", answer or "(no answer)", [source.citation for source in sources])
    print(f"Top-1 retrieval on in-scope questions: {hits}/{evaluated} ({hits / evaluated:.1%})")
except (RuntimeError, OSError, ValueError) as error:
    parser.exit(1, f"Error: {error}\n")
