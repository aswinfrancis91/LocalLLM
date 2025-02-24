import chromadb
from llama_index.core import VectorStoreIndex, SummaryIndex
from llama_index.core.schema import IndexNode
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from config import PERSIST_DIR_CODE, PERSIST_DIR_TEXT, CODE_EMBED_MODEL, TEXT_EMBED_MODEL, LLM_MODEL

# Persistent clients for code and text
code_chroma_client = chromadb.PersistentClient(path=PERSIST_DIR_CODE)
text_chroma_client = chromadb.PersistentClient(path=PERSIST_DIR_TEXT)

# Fetch code index
code_chroma_collection = code_chroma_client.get_or_create_collection(name="code_index")
code_vector_store = ChromaVectorStore(chroma_collection=code_chroma_collection)
code_storage_context = StorageContext.from_defaults(vector_store=code_vector_store)
code_index = VectorStoreIndex.from_vector_store(vector_store=code_vector_store,
                                                storage_context=code_storage_context,
                                                embed_model=CODE_EMBED_MODEL)
code_index_retriever = code_index.as_retriever(similarity_top_k=2)

# Fetch text index
text_chroma_collection = text_chroma_client.get_or_create_collection(name="text_index")
text_vector_store = ChromaVectorStore(chroma_collection=text_chroma_collection)
text_storage_context = StorageContext.from_defaults(vector_store=text_vector_store)
text_index = VectorStoreIndex.from_vector_store(vector_store=text_vector_store,
                                                storage_context=text_storage_context,
                                                embed_model=TEXT_EMBED_MODEL)
text_index_retriever = text_index.as_retriever(similarity_top_k=2)

# Create a SummaryIndex combining both indices
text_obj = IndexNode(
    index_id="text", obj=text_index_retriever
)
code_obj = IndexNode(
    index_id="code", obj=code_index_retriever
)
summary_index = SummaryIndex(objects=[text_obj, code_obj])

# Query engine setup
query_engine = summary_index.as_query_engine(llm=LLM_MODEL)

query = "How does authentication work in this project?"
response = query_engine.query(query)
print("AI Response:", response)
