from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

# load model once (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text: str) -> list[float]:
    """
    Generate embedding for given text
    """
    if not text:
        return []

    embedding = model.encode(text)

    return embedding.tolist()