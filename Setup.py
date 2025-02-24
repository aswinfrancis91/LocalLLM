from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma.base import ChromaVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
import chromadb
from dotenv import load_dotenv
import os
import logging

load_dotenv()  # Load environment variables from .env file

logging.basicConfig(level=logging.DEBUG)

repo_path = os.getenv("SOURCE_PATH")

# Load and separate doc types
all_docs = SimpleDirectoryReader(
    input_dir=repo_path,
    recursive=True,
    required_exts=[".cs", ".json", ".md", ".ts", ".css", ".csproj", ".sln", ".yaml"],
    exclude=["node_modules",".idea",".azuredevops",".vscode",".git",".gitignore",".vs","bin"]
).load_data()

# Separate documents into code files and text files
code_extensions = {".cs", ".ts", ".css", ".csproj", ".sln", ".yaml"}
text_extensions = {".md", ".json"}

code_docs = [doc for doc in all_docs if os.path.splitext(doc.metadata.get("file_path", ""))[1] in code_extensions]
text_docs = [doc for doc in all_docs if os.path.splitext(doc.metadata.get("file_path", ""))[1] in text_extensions]

print(f"Loaded {len(code_docs)} code documents.")
print(f"Loaded {len(text_docs)} text documents.")


# Define where to store the index
persist_dir = os.getenv("PERSIST_DIR")

# Set up ChromaDB for local vector storage
chroma_client = chromadb.PersistentClient(path=persist_dir)

# Set up CodeBERT for code embeddings
code_bert_embed_model = HuggingFaceEmbedding(model_name="microsoft/codebert-base")
code_chroma_collection = chroma_client.get_or_create_collection(name="code_index")
code_vector_store = ChromaVectorStore(chroma_collection=code_chroma_collection)

# Create and persist code index
code_storage_context = StorageContext.from_defaults(vector_store=code_vector_store)
code_index = VectorStoreIndex.from_documents(code_docs, storage_context=code_storage_context,
                                             embed_model=code_bert_embed_model)
code_index.storage_context.persist()

# Set up MiniLM-L6-v2 for text/documentation embeddings
text_embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_chroma_collection = chroma_client.get_or_create_collection(name="text_index")
text_vector_store = ChromaVectorStore(chroma_collection=text_chroma_collection)

# Create and persist text index
text_storage_context = StorageContext.from_defaults(vector_store=text_vector_store)
text_index = VectorStoreIndex.from_documents(text_docs, storage_context=text_storage_context,
                                             embed_model=text_embed_model)
text_index.storage_context.persist()

print("Finished creating and persisting indices.")


