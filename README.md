# LocalLLM: Build a Lightweight Local Search and Embedding System

## Overview

LocalLLM is a project for creating a local embedding and search engine for codebases using [LlamaIndex](https://github.com/jerryjliu/llama_index). It connects with Ollama (a local LLM model) and uses other open-source libraries to transform your local repository into an efficient vector-based information retrieval system.

This system supports lightweight local storage, prioritizes data privacy, and empowers developers to query code repositories effectively without relying on external APIs like OpenAI.

---

## Features

- **Local Vector Store with ChromaDB**: Provides private, local performance for storing generated embeddings.
- **Embedding Models Powered by HuggingFace**: Uses `sentence-transformers/all-MiniLM-L6-v2` for lightweight and efficient embeddings.
- **Support for Local LLM Models**: Integration with `codellama:7b-instruct` through Ollama for optimized local querying.
- **Extensive File Support**: Indexes common codebase files like `.cs`, `.json`, `.md`, `.yaml`, `.ts`, `.css`, `.csproj`, `.sln`, and more.
- **Persistent Data Storage**: Indexes can be stored locally and reused across multiple sessions.
- **Customizable Environment**: Paths and configurations are managed through a simple `.env` file.

---

## Installation

### 1. Prerequisites

- **Python 3.9+**: Ensure it is installed on your system.
- **Local LLM Model**: Obtain and serve a local LLM model via [Ollama](https://ollama.com/).

### 2. Install Required Libraries

Run the following commands to install the required dependencies:

```bash
pip install llama-index llama-index-llms-ollama llama-index-embeddings-huggingface
pip install llama-index-vector-stores-chroma chromadb
pip install tiktoken
```

### 3. Clone the Repository

Clone the repository or integrate the required code into your project:
```bash
git clone <repository-url>
cd <repository-name>
```

---

## How It Works

The project uses **LlamaIndex**, **ChromaDB**, and **HuggingFace embedding models** to create a fully local and efficient system for codebase indexing and querying. Below is the high-level workflow:

1. **Load your Repository**:  
   Specify the `SOURCE_PATH` with your desired codebase using the `.env` file. You can also override file types that need indexing.

2. **Generate Vector Embeddings**:  
   Leverages the `sentence-transformers/all-MiniLM-L6-v2` model to create embeddings.

3. **Persist and Reuse the Index**:  
   The generated embeddings and index are stored locally in the `PERSIST_DIR`. Reusing stored indices removes the need for re-processing.

4. **Query your Codebase**:  
   Using Codellama (`codellama:7b-instruct`) served locally via Ollama, query your codebase efficiently and retrieve results locally.

---

## Configuration

Set configurations in the `.env` file:

```dotenv
PERSIST_DIR=/path/to/store/index_store        # Path to save persistent embeddings
SOURCE_PATH=/path/to/your/codebase           # Path to the codebase for indexing
```

### Example `.env`

```dotenv
PERSIST_DIR=D:\IndexStore
SOURCE_PATH=D:\SourceCode
```

---

## Usage

### Indexing your Codebase

First, ensure your `.env` file is configured correctly, then trigger the indexing process using the `setup.py` script:

```python
from setup import run_indexing

# Trigger the indexing process
run_indexing()
```

The steps performed:
1. Code files are read recursively from the `SOURCE_PATH`.
2. Vector embeddings are generated for the files.
3. Embeddings are stored in the `PERSIST_DIR` directory.

### Querying the Index

After creating the index, you can query it to retrieve insights or code suggestions. Execute the `query.py` script or use the following sample code:

```python
from query import query_engine

query = "Write unit test using nunit and moq for AuthenticatedPing() method in PingController"
response = query_engine.query(query)
print("AI Response:", response)
```

This leverages `codellama:7b-instruct` and the index to provide relevant and actionable insights.

---

## Folder Structure

```plaintext
.
├── config.py           # Configuration module (reads environment variables)
├── setup.py            # Indexing script - loads and processes codebase
├── query.py            # Query module for performing searches on the index
├── .env                # Environment file (paths for persist and source)
├── README.md           # Project documentation
└── index_store         # Stores index and embeddings locally
```

---

## Example Code Usage

### Embedding & Indexing Pipeline

The `setup.py` script provides an efficient indexing mechanism:

```python
python setup.py
```

### Query Example

Using the `query.py` script:

```python
python query.py
```

---

## Known Issues and Limitations

- The project currently supports specific file types (e.g., `.cs`, `.json`, `.ts`). If your project uses additional file extensions, ensure to include them in the `SimpleDirectoryReader` configurations within `setup.py`.
- Ensure that both `PERSIST_DIR` and `SOURCE_PATH` in the `.env` file are valid and accessible.
- Long response queries may take time due to the reliance on large language models.

---

## Future Plans

1. **Enhanced File Type Support**: Expand support for additional code and documentation formats.
2. **Performance Optimization**: Optimize indexing and querying speed.
3. **Interactive UI**: Add support for a web-based or CLI-driven interactive querying experience.
4. **Extensive Query Examples**: Provide additional examples for common developer use cases.

---

## Contributing

Feel free to fork this repository, submit issues, or propose new features via pull requests! Please ensure your contributions align with the goal of creating a lightweight, private, and efficient local indexing and querying platform.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.