from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.chroma.base import ChromaVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
import chromadb
import logging
from config import SOURCE_PATH, PERSIST_DIR, CODE_INDEX, EMBED_MODEL

logging.basicConfig(level=logging.DEBUG)

# Load code and related files
all_docs = SimpleDirectoryReader(
    input_dir=SOURCE_PATH,
    recursive=True,
    required_exts=[".cs", ".json", ".md", ".ts", ".css", ".csproj", ".sln", ".yaml"],
    exclude=["node_modules", ".idea", ".azuredevops", ".vscode", ".git", ".gitignore", ".vs", "bin"]
).load_data()

# Create a persistent client for indices
chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)

# Create code index
chroma_collection = chroma_client.get_or_create_collection(name=CODE_INDEX)
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
code_index = VectorStoreIndex.from_documents(all_docs, storage_context=storage_context, embed_model=EMBED_MODEL)
code_index.storage_context.persist(persist_dir=PERSIST_DIR)

print("Finished creating and persisting indices.")
