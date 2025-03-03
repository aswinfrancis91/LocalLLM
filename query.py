import logging
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from config import PERSIST_DIR, EMBED_MODEL, CODE_INDEX, LLM_MODEL

logging.basicConfig(level=logging.DEBUG)

# Initialize a persistent ChromaDB client with the specified directory
chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)

# Retrieve or create a collection in ChromaDB by using the provided collection name
chroma_collection = chroma_client.get_or_create_collection(name=CODE_INDEX)

# Set up a vector store using the retrieved or created ChromaDB collection
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Create a storage context by combining default configurations and the vector store
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Build a vector store index by linking the vector store, storage context, and embedding model
index = VectorStoreIndex.from_vector_store(vector_store=vector_store,
                                                storage_context=storage_context,
                                                embed_model=EMBED_MODEL)

# Generate a query engine from the index using a specific language model (LLM)
query_engine = index.as_query_engine(llm=LLM_MODEL)

query = "Write unit test using nunit and moq for AuthenticatedPing() method in PingController"
response = query_engine.query(query)
print("AI Response:", response)
