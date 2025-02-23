# LocalLLM: Build a Lightweight Local Search and Embedding System

## Overview

LocalLLM is a project for creating a local embedding and search engine for codebases using [LlamaIndex](https://github.com/jerryjliu/llama_index). It connects with Ollama (a local LLM model) and uses other open-source libraries to transform your local repository into an efficient vector-based information retrieval system.

This system supports lightweight local storage, focuses on privacy, and allows developers to query across their repositories effectively with no dependency on external APIs like OpenAI.

---

## Features

- **Local Vector Store with ChromaDB**: Embeddings are stored in ChromaDB, ensuring data privacy.
- **Local Model Support**: Use HuggingFace models for embeddings.
- **Extensive File Support**: Indexes `.cs`, `.json`, `.md`, `.yaml`, `.ts`, `.css`, `.csproj`, and `.sln` file extensions.
- **Persistent Index Storage**: Save indexes locally, allowing reuse across multiple sessions.
- **Environment Configuration**: Easily adaptable configuration using `.env` files.

---

## Installation

### 1. Prerequisites

Ensure you have Python 3.9+ installed. You also need a local LLM model served by [Ollama](https://ollama.com/).

### 2. Install Required Libraries

Install the necessary libraries with pip:

```bash
pip install llama-index llama-index-llms-ollama llama-index-embeddings-huggingface
pip install llama-index-vector-stores-chroma chromadb
pip install tiktoken
```

- **`llama-index`**: Core library for indexing and retrieval.
- **`llama-index-llms-ollama`**: Connects LlamaIndex to Ollama's local LLM.
- **`llama-index-embeddings-huggingface`**: Leverages HuggingFace embeddings for local functionality.
- **`chromadb`**: Lightweight vector database for storing embeddings.

---

## How It Works

The project uses **LlamaIndex (formerly GPT Index)**, **HuggingFace Embedding Models**, and **ChromaDB** to locally index codebases. The workflow is as follows:

1. **Load your Repository**: 
   - Specify the source directory in the `.env` file under `SOURCE_PATH`. You can customize the file extensions you’d like indexed.
2. **Generate Embeddings**: 
   - Use a HuggingFace model to generate vector embeddings for each document.
3. **Store Embeddings Locally**: 
   - Use a local persistent client with ChromaDB to store and reuse the embeddings.
4. **Query Locally**: 
   - Perform search or query operations on your local codebase.

---

## Configuration

All important paths can be customized using the `.env` file:

```dotenv
PERSIST_DIR=/path/to/store/index_store        # Where embeddings will be stored
SOURCE_PATH=/path/to/your/codebase           # Path to the codebase to index
```

### Example Configuration

```dotenv
PERSIST_DIR=D:\Development\Personal\Llamaindex\index_store
SOURCE_PATH=D:\Development\UnifiedDropShip
```

---

## Usage

### Setting Up the Codebase

1. Clone this repository or integrate it into your project.
2. Configure the `.env` file with your repository path (`SOURCE_PATH`) and persistence directory (`PERSIST_DIR`).

### Run the Indexer

```python
from setup import run_indexing

# Trigger the indexing process
run_indexing()
```

The indexing process:
- Loads documents from the source directory.
- Generates embeddings.
- Persists these embeddings in the `index_store` directory for future use.

### Querying

Setup your local model and query the index to retrieve relevant information from your codebase.

More query and usage examples will be documented in future updates.

---

## Folder Structure

```plaintext
.
├── setup.py            # Core setup script for indexing
├── .env                # Environment file for paths
├── README.md           # Project documentation
└── index_store         # Directory to store the embeddings
```

---

## Known Issues and Future Plans

### Known Issues

- Only files with the specified extensions are indexed. Make sure to include extensions for new formats in `SimpleDirectoryReader`.
- Ensure all library dependencies are installed, or you may encounter compatibility issues.

### Future Enhancements

- Add query examples for common use cases.
- Extend indexing to support more file formats automatically.
- Improve performance for larger repositories.

---

## References

- [LlamaIndex Documentation](https://gpt-index.readthedocs.io/)
- [ChromaDB Documentation](https://chromadb.readthedocs.io/)
- [HuggingFace Models](https://huggingface.co/)

---

If you encounter issues or want to contribute, feel free to open a pull request or raise an issue. Happy coding!