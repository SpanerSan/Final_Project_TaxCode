# Design decisions

- **Source.** The public Әділет page required JavaScript to render the legal text in the initial lookup. The checkpoint uses an official government PDF for a reproducible snapshot and links to the exact PDF pages.
- **Passage size.** Keep article and provision identifiers with each excerpt. During extraction, the initial line ranges cut off several sentences and put the end of Article 503(2) into the next chunk. The inspection caught this and the extraction boundaries were corrected before testing.
- **Vector storage.** The checkpoint indexes nine passages in memory. Cosine search over that small set avoids a database installation. The local search uses weighted text vectors. The API mode uses model-generated embeddings.
- **Citations.** The model selects source IDs and the app builds the citation text and links from source metadata. This prevents invented source IDs from becoming printed citations. Whether a valid citation supports the answer still needs to be reviewed when evaluating generated responses.
- **Verification.** The local search was run against the checkpoint questions. API request and citation handling were checked with simulated responses because the development environment had no configured API key.
