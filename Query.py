from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext, VectorStoreIndex
import chromadb
import logging
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

logging.basicConfig(level=logging.DEBUG)
# Define paths
persist_dir = os.getenv("PERSIST_DIR", "default_path_if_not_set")

# Load ChromaDB storage
chroma_client = chromadb.PersistentClient(path=persist_dir)
chroma_collection = chroma_client.get_or_create_collection(name="codebase_index")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load the index from storage
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context, embed_model=embed_model)

# Set up CodeLlama via Ollama
llm = Ollama(model="codellama:7b-instruct", request_timeout=1800)  # Modify if needed

# Create a query engine
query_engine = index.as_query_engine(llm=llm)

# Test query
query = "How does authentication work in this project?"
response = query_engine.query(query)
print("📝 AI Response:", response)
