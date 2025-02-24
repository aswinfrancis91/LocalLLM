from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext, VectorStoreIndex, ComposableGraph
from llama_index.core.settings import default_settings
import chromadb
import logging
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

logging.basicConfig(level=logging.DEBUG)
# Define paths
persist_dir = os.getenv("PERSIST_DIR")

# Load ChromaDB storage
chroma_client = chromadb.PersistentClient(path=persist_dir)

# Define and set the default embedding model globally
hf_embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
default_settings.embed_model = hf_embed_model  # Set Hugging Face embeddings as the global default

# Load code index
code_chroma_collection = chroma_client.get_or_create_collection(name="code_index")
code_vector_store = ChromaVectorStore(chroma_collection=code_chroma_collection)
code_bert_embed_model = HuggingFaceEmbedding(model_name="microsoft/codebert-base")
code_storage_context = StorageContext.from_defaults(vector_store=code_vector_store)
code_index = VectorStoreIndex.from_vector_store(vector_store=code_vector_store,
                                                storage_context=code_storage_context,
                                                embed_model=code_bert_embed_model)

# Load text index
text_chroma_collection = chroma_client.get_or_create_collection(name="text_index")
text_vector_store = ChromaVectorStore(chroma_collection=text_chroma_collection)
#text_embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_storage_context = StorageContext.from_defaults(vector_store=text_vector_store)
text_index = VectorStoreIndex.from_vector_store(vector_store=text_vector_store,
                                                storage_context=text_storage_context,
                                                embed_model=hf_embed_model)
# Set up CodeLlama via Ollama
llm = Ollama(model="codellama:7b-instruct", request_timeout=1800)

# Combine Indices with ComposableGraph
# Specify the root index type (VectorStoreIndex) and child indices with summaries
composed_index = ComposableGraph.from_indices(
    root_index_cls=VectorStoreIndex,  # Root index type
    children_indices=[code_index, text_index],  # Child indices
    index_summaries=[
        "This index contains all source code files from the project repository.",
        "This index contains all text-based documentation and metadata files."
    ],  # Summaries for each index
    embed_model=hf_embed_model  # Explicit embedding model

)




# Create a query engine for the composed index
query_engine = composed_index.as_query_engine(llm=llm)

# Test query
query = "How does authentication work in this project?"
response = query_engine.query(query)
print(" AI Response:", response)
