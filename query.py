import logging
import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from config import PERSIST_DIR, EMBED_MODEL, CODE_INDEX, LLM_MODEL

logging.basicConfig(level=logging.DEBUG)

# Persistent clients for code and text
chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)

# Fetch code index
chroma_collection = chroma_client.get_or_create_collection(name=CODE_INDEX)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store,
                                                storage_context=storage_context,
                                                embed_model=EMBED_MODEL)

query_engine = index.as_query_engine(llm=LLM_MODEL)

query = "Write unit test using nunit and moq for AuthenticatedPing() method in PingController"
response = query_engine.query(query)
print("AI Response:", response)
