"""Terminal entry point for the Kazakhstan Tax Code checkpoint."""

import argparse
import json
from pathlib import Path

from rag import OpenAI, Passage, VectorIndex

ROOT = Path(__file__).resolve().parent
NO_ANSWER = "В выбранных фрагментах Налогового кодекса ответа не найдено."


def load_corpus():
    data = json.loads((ROOT / "data" / "vat.json").read_text(encoding="utf-8"))
    return data["code"], [Passage(**row, source=data["source"]) for row in data["passages"]]


def display_sources(passages):
    for passage in passages:
        print(f"- {passage.citation} — {passage.title}\n  {passage.url}")


def run(question, index, provider):
    passages = index.search(question)
    if provider:
        answer, sources = provider.answer(question, passages)
        print(answer or NO_ANSWER)
        if sources:
            print("\nИсточники")
            display_sources(sources)
    elif passages:
        print("Поиск по источнику. Найденный фрагмент:")
        print(passages[0].text)
        print()
        display_sources(passages[:1])
    else:
        print(NO_ANSWER)


def main():
    parser = argparse.ArgumentParser(description="Search selected VAT provisions in the Kazakhstan Tax Code.")
    parser.add_argument("question", nargs="?", help="Question, preferably in Russian")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--search", action="store_true", help="Local vector search with source excerpts")
    modes.add_argument("--llm", action="store_true", help="Use OpenAI for embeddings and grounded answers")
    args = parser.parse_args()
    if args.question is not None and not args.question.strip():
        parser.error("Enter a non-empty question.")

    try:
        provider = OpenAI.from_environment(ROOT / ".env") if args.llm else None
        code, passages = load_corpus()
        index = VectorIndex(passages, provider)
        print(f"Учебный корпус: {code}, фрагменты статей 502–506.")
        if args.question is not None:
            run(args.question, index, provider)
            return
        while True:
            try:
                question = input("\nВопрос по НДС (Enter для выхода): ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return
            if not question:
                return
            run(question, index, provider)
    except (RuntimeError, OSError, ValueError) as error:
        parser.exit(1, f"Ошибка: {error}\n")


if __name__ == "__main__":
    main()
