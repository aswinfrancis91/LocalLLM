from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores import ChromaVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

repo_path = os.getenv("SOURCE_PATH", "default_path_if_not_set")

# Only load .cs, .json, and .md files
docs = SimpleDirectoryReader(
    input_dir=repo_path,
    recursive=True,
    required_exts=[".cs", ".json", ".md", ".ts", ".css", ".csproj", ".sln"".yaml"]  # Specify allowed extensions
).load_data()

print(f"Loaded {len(docs)} documents.")

# Define where to store the index
persist_dir = os.getenv("PERSIST_DIR", "default_path_if_not_set")

# Set up ChromaDB for local vector storage
chroma_client = chromadb.PersistentClient(path=persist_dir)
chroma_collection = chroma_client.get_or_create_collection(name="codebase_index")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Use a specific local embedding model
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Store the index
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(docs, storage_context=storage_context, embed_model=embed_model)

# persist index
index.storage_context.persist()