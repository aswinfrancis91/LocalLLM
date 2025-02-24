import os
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

# Load environment variables
load_dotenv()

# Persist directories for code and text
PERSIST_DIR = os.getenv("PERSIST_DIR")  # E.g., "D:/Development/IndexStore/Code"

# Source path for documents (if needed)
SOURCE_PATH = os.getenv("SOURCE_PATH")

# Embedding models
EMBED_MODEL = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")  # For text

# LLM Model
LLM_MODEL = Ollama(model="codellama:7b-instruct", request_timeout=1800)

CODE_INDEX= "code_index"
