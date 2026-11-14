# Tax Code Assistant plan

## November 16 checkpoint

1. Build the terminal app around a small Russian-language corpus from the Kazakhstan Tax Code. Start with the VAT provisions in Chapter 51 and record the article numbers and official source.
2. Index the text as vectors. Use cosine similarity to retrieve relevant provisions for a question.
3. Send the question and retrieved provisions to an LLM. Validate the article IDs it returns and build the official citations in the application.
4. Add a no-key mode to demonstrate vector retrieval and display source passages. Document how to run both modes.
5. Check the CLI on ten fixed questions, including questions outside the VAT sample. Record which tests use the real provider and which use local retrieval or a test double.
6. Commit the plan, agent instructions, first session log, and runnable checkpoint to GitHub.

## December 13 code freeze

Expand coverage, review the full set of 30 questions, measure answer correctness and citation quality, compare with the baseline, and complete the team reflection. Tag the final commit as v1.0.

## Team responsibilities

- Rashid: source data, embeddings, and retrieval.
- Nadir: terminal app, evaluation, and repository documentation.
- Both: review the checkpoint, keep agent logs, and make their own contributions.
