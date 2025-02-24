import os
from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.chroma.base import ChromaVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
import chromadb
import logging
from config import SOURCE_PATH, PERSIST_DIR_CODE, PERSIST_DIR_TEXT, CODE_EMBED_MODEL, TEXT_EMBED_MODEL

logging.basicConfig(level=logging.DEBUG)

# Load and separate documents
all_docs = SimpleDirectoryReader(
    input_dir=SOURCE_PATH,
    recursive=True,
    required_exts=[".cs", ".json", ".md", ".ts", ".css", ".csproj", ".sln", ".yaml"],
    exclude=["node_modules", ".idea", ".azuredevops", ".vscode", ".git", ".gitignore", ".vs", "bin"]
).load_data()

code_extensions = {".cs", ".ts", ".css", ".csproj", ".sln", ".yaml"}
text_extensions = {".md", ".json"}

code_docs = [doc for doc in all_docs if os.path.splitext(doc.metadata.get("file_path", ""))[1] in code_extensions]
text_docs = [doc for doc in all_docs if os.path.splitext(doc.metadata.get("file_path", ""))[1] in text_extensions]

print(f"Loaded {len(code_docs)} code documents.")
print(f"Loaded {len(text_docs)} text documents.")

# Create a persistent client for code and text indices
code_chroma_client = chromadb.PersistentClient(path=PERSIST_DIR_CODE)
text_chroma_client = chromadb.PersistentClient(path=PERSIST_DIR_TEXT)

# Create code index
code_chroma_collection = code_chroma_client.get_or_create_collection(name="code_index")
code_vector_store = ChromaVectorStore(chroma_collection=code_chroma_collection)
code_storage_context = StorageContext.from_defaults(vector_store=code_vector_store)
code_index = VectorStoreIndex.from_documents(code_docs, storage_context=code_storage_context,
                                             embed_model=CODE_EMBED_MODEL)
code_index.storage_context.persist()

# Create text index
text_chroma_collection = text_chroma_client.get_or_create_collection(name="text_index")
text_vector_store = ChromaVectorStore(chroma_collection=text_chroma_collection)
text_storage_context = StorageContext.from_defaults(vector_store=text_vector_store)
text_index = VectorStoreIndex.from_documents(text_docs, storage_context=text_storage_context,
                                             embed_model=TEXT_EMBED_MODEL)
text_index.storage_context.persist()

print("Finished creating and persisting indices.")
