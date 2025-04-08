import os
import argparse
import logging
from pathlib import Path
from typing import List

from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from sentence_transformers import SentenceTransformer

import fitz  # PyMuPDF

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_text_from_file(file_path: Path) -> str:
    try:
        if file_path.suffix == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif file_path.suffix == ".md":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif file_path.suffix == ".pdf":
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            return text
        else:
            logger.warning(f"Unsupported file type: {file_path.suffix}")
            return ""
    except Exception as e:
        logger.error(f"Failed to read {file_path}: {e}")
        return ""


def chunk_text(text: str, max_tokens: int = 500) -> List[str]:
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) > max_tokens:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            current_chunk += " " + sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


def create_collection_if_needed(client: QdrantClient, collection_name: str, dim: int):
    collections = client.get_collections().collections
    if not any(c.name == collection_name for c in collections):
        logger.info(f"Creating new collection: {collection_name}")
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )
    else:
        logger.info(f"Collection '{collection_name}' already exists.")


def index_files(data_dir: str, collection_name: str, model, client: QdrantClient):
    files = list(Path(data_dir).rglob("*.*"))
    logger.info(f"Found {len(files)} files in {data_dir}")

    points = []
    idx = 0

    for file_path in tqdm(files, desc="Indexing files", unit="file"):
        text = extract_text_from_file(file_path)
        if not text:
            continue
        chunks = chunk_text(text)
        for chunk in chunks:
            embedding = model.encode(chunk).tolist()
            points.append(PointStruct(
                id=idx,
                vector=embedding,
                payload={"text": chunk, "source": str(file_path)}
            ))
            idx += 1

    logger.info(f"Uploading {len(points)} vectors to Qdrant")
    client.upsert(collection_name=collection_name, points=points)


def main():
    parser = argparse.ArgumentParser(description='Index files into Qdrant')
    parser.add_argument('--data-dir', default='/qdrant/data', help='Path to data directory')
    parser.add_argument('--collection-name', default='local-docs', help='Qdrant collection name')
    args = parser.parse_args()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    client = QdrantClient(host="localhost", port=6333)

    create_collection_if_needed(client, args.collection_name, model.get_sentence_embedding_dimension())
    index_files(args.data_dir, args.collection_name, model, client)


if __name__ == "__main__":
    main()
