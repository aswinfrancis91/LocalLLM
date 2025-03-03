from llama_index.core import SimpleDirectoryReader
from llama_index.vector_stores.chroma.base import ChromaVectorStore
from llama_index.core import StorageContext, VectorStoreIndex
import chromadb
import logging
from config import SOURCE_PATH, PERSIST_DIR, CODE_INDEX, EMBED_MODEL

logging.basicConfig(level=logging.DEBUG)

# Load all relevant documents from the specified source directory
# This includes files with specific extensions such as .cs, .json, .md, etc.
# Excludes certain directories like 'node_modules', '.git', etc., to avoid unnecessary files
all_docs = SimpleDirectoryReader(
    input_dir=SOURCE_PATH,
    recursive=True,
    required_exts=[".cs", ".json", ".md", ".ts", ".css", ".csproj", ".sln", ".yaml"],
    exclude=["node_modules", ".idea", ".azuredevops", ".vscode", ".git", ".gitignore", ".vs", "bin"]
).load_data()

# Initialize a persistent ChromaDB client with the specified directory
chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)

# Retrieve or create a collection in ChromaDB by using the provided collection name
chroma_collection = chroma_client.get_or_create_collection(name=CODE_INDEX)

# Set up a vector store using the retrieved or created ChromaDB collection
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Create a storage context by combining default configurations and the vector store
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Build a vector store index from all loaded documents, embedding the data for efficient querying
code_index = VectorStoreIndex.from_documents(all_docs, storage_context=storage_context, embed_model=EMBED_MODEL)

# Persist the created vector store index for reuse in the specified directory
code_index.storage_context.persist(persist_dir=PERSIST_DIR)

print("Finished creating and persisting indices.")
