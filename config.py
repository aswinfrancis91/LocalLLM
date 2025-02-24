import os
from dotenv import load_dotenv
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

# Load environment variables
load_dotenv()

# Persist directories for code and text
PERSIST_DIR_CODE = os.getenv("PERSIST_DIR_CODE")  # E.g., "D:/Development/IndexStore/Code"
PERSIST_DIR_TEXT = os.getenv("PERSIST_DIR_TEXT")  # E.g., "D:/Development/IndexStore/Text"

# Source path for documents (if needed)
SOURCE_PATH = os.getenv("SOURCE_PATH")

# Embedding models
CODE_EMBED_MODEL = HuggingFaceEmbedding(model_name="microsoft/codebert-base")  # For code
TEXT_EMBED_MODEL = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")  # For text

# LLM Model
LLM_MODEL = Ollama(model="codellama:7b-instruct", request_timeout=1800)

# Other default settings and global service context if needed
