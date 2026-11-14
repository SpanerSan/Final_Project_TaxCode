import json
import unittest
from unittest.mock import patch

from main import load_corpus
from rag import OpenAI, VectorIndex


class GroundedAnswerTests(unittest.TestCase):
    def setUp(self):
        _, passages = load_corpus()
        self.passage = next(item for item in passages if item.article == 503 and item.point == "п. 1")
        self.provider = OpenAI("test-key", "embedding-test", "generation-test")

    def response(self, ids):
        return {
            "status": "completed",
            "output": [{"type": "message", "content": [{
                "type": "output_text",
                "text": json.dumps({"answer": "Тестовый ответ", "source_ids": ids}),
            }]}],
        }

    def test_retrieval_and_response_path(self):
        def fake_post(endpoint, payload):
            if endpoint == "embeddings":
                return {"data": [{"index": 0, "embedding": [1.0, 0.0]}]}
            self.assertEqual(endpoint, "responses")
            source = json.loads(payload["input"])["sources"][0]
            self.assertEqual(source["text"], self.passage.text)
            return self.response(["S1"])

        with patch.object(self.provider, "post", side_effect=fake_post):
            index = VectorIndex([self.passage], self.provider)
            answer, sources = self.provider.answer("Какая базовая ставка НДС?", index.search("НДС"))
        self.assertEqual(answer, "Тестовый ответ")
        self.assertEqual(sources[0].citation, "Ст. 503, п. 1")
        self.assertTrue(sources[0].url.endswith("#page=697"))

    def test_unknown_source_id_is_discarded(self):
        with patch.object(self.provider, "post", return_value=self.response(["S999"])):
            self.assertEqual(self.provider.answer("Test question", [self.passage]), ("", []))


if __name__ == "__main__":
    unittest.main()
