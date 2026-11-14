# Tax Code Assistant

Narxoz University CSS4007 Artificial Intelligence project by Rashid Mukashev and Nadir Bairamov.

The checkpoint is a terminal app for searching selected Russian-language VAT provisions from the Kazakhstan Tax Code. It prints an article, provision number, and link to the official source. With OpenAI API access it retrieves evidence using embeddings and generates an answer from that evidence.

## Run the checkpoint

Requirements: Python 3.11 or later. The Python standard library is sufficient.

```sh
git clone https://github.com/SpanerSan/Final_Project_TaxCode.git
cd Final_Project_TaxCode
python3 main.py --search "Какая базовая ставка НДС?"
```

The default mode and `--search` use local weighted word vectors and cosine similarity. They display the top source excerpt, including the article number and the PDF page. Omit the question to use the interactive prompt.

To generate an answer, set `OPENAI_API_KEY` in your environment or copy `.env.example` to `.env` and set the key there. Then run:

```sh
python3 main.py --llm "Какой срок подачи декларации по НДС?"
```

In this mode the app embeds the passages and question, ranks passages by cosine similarity, and sends the four highest-ranked passages to the model. The model returns the answer and IDs of supporting passages. The app validates the IDs and creates citations using the stored article, provision, and source URL. The default models are `text-embedding-3-small` and `gpt-4.1-mini`. The API receives the question and selected passages in generation mode.

## Data

`data/vat.json` contains nine selected passages from Articles 502–506 of the [officially published Tax Code PDF](https://www.gov.kz/api/v1/public/assets/2026/6/15/8ec094fb07c909eda80931a562901431_original.5413202.pdf) (Law No. 214-VIII of 18 July 2025, PDF pages 696–699). The passages retain the source wording with line breaks joined. Topic labels are search metadata. The [code record in Әділет](https://adilet.zan.kz/rus/docs/K2500000214) can be used to check updates. The bundled sample is static and limited to these VAT provisions.

## Checkpoint evaluation

```sh
python3 evaluate.py
python3 -m unittest discover -s tests -v
python3 evaluate.py --llm  # Requires an OpenAI API key
```

The local retrieval check returned the expected article and provision as the top result for all 9 in-scope questions. The tenth question was about divorce and returned no match. The test set is a small checkpoint sample. The automated API tests use simulated responses. Live answer generation, answer faithfulness, and citation correctness still need to be evaluated against the provider.

The December release plan covers expansion of the corpus, manual review of answers and citations on 30 questions, and comparison against an LLM without retrieval.

## Project records

- [Plan](PLAN.md)
- [Agent instructions](AGENTS.md)
- [First agent session](agent-logs/01-checkpoint-build.md)
- [Design decisions](DECISIONS.md)
