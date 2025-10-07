# Nexus RAG Engine

Nexus is a groundbreaking, command-line AI tool for live knowledge retrieval. It ingests knowledge directly from a web URL and allows you to ask questions about it in an interactive session.

This tool demonstrates an advanced Retrieval-Augmented Generation (RAG) architecture, featuring live data ingestion and TF-IDF based semantic search.

## Features

- **Live Knowledge Ingestion:** Works with any public, text-based web page (e.g., Wikipedia articles).
- **Semantic Search:** Uses a TF-IDF vectorizer to find contextually relevant information, not just keyword matches.
- **Verifiable Source Citation:** Every answer is accompanied by the exact quotes from the source material used for generation.
- **Interactive Nexus Mode:** An interactive chat mode for conversational Q&A.

## Setup and Installation

This project uses Python and requires the dependencies listed in `requirements.txt`.

1.  **Create a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the engine by providing a URL. If no URL is provided, it will default to the Wikipedia article on Artificial Intelligence.

```bash
nexus_cli.py [URL]
```

**Example:**

```bash
python nexus_cli.py https://en.wikipedia.org/wiki/World_War_II
```

Once the knowledge base is ingested and vectorized, you will be dropped into an interactive prompt where you can ask questions.

```
Initializing Nexus Engine. Ingesting knowledge from: https://en.wikipedia.org/wiki/World_War_II
Knowledge base ingested successfully. (1523 sentences)
Semantic vectorization complete. Ready for queries.

--- Nexus Interactive Mode ---
Ask a question, or type 'exit' to quit.
> What were the main causes of the war?

==================== NEXUS RESPONSE ====================
Based on the retrieved context, here is an answer to 'What were the main causes of the war?':
...

"The immediate cause of the war in Europe was the German invasion of Poland on 1 September 1939 and the subsequent declarations of war on Germany by France and the United Kingdom."

"Key long-term causes included the rise of fascism in Europe, the unresolved issues of World War I, and the aggressive expansionist policies of Germany, Italy, and Japan."
------------------------------------------------------
Citations:
  [1] The immediate cause of the war in Europe was the German invasion of Poland on 1 S...
  [2] Key long-term causes included the rise of fascism in Europe, the unresolved is...
======================================================

> exit
```
