from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import os
from pathlib import Path
import logging
from typing import List, Dict, Optional
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_text_from_file(file_path: Path) -> str:
    """Extract text from a file based on its extension."""
    try:
        if file_path.suffix == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif file_path.suffix == ".md":
            import markdown
            with open(file_path, "r", encoding="utf-8") as f:
                return markdown.markdown(f.read())
        elif file_path.suffix == ".pdf":
            from io import StringIO
            from pdfminer.converter import TextConverter
            from pdfminer.layout import LAParams
            from pdfminer.pdfdocument import PDFDocument
            from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
            from pdfminer.pdfpage import PDFPage
            from pdfminer.pdfparser import PDFParser
            
            output_string = StringIO()
            with open(file_path, 'rb') as in_file:
                parser = PDFParser(in_file)
                doc = PDFDocument(parser)
                rsrcmgr = PDFResourceManager()
                device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                
                for page in PDFPage.create_pages(doc):
                    interpreter.process_page(page)
            
            return output_string.getvalue()
        else:
            logger.error(f"Unsupported file type: {file_path.suffix}")
            return ""
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return ""

def create_qdrant_collection(client: QdrantClient, collection_name: str) -> None:
    """Create Qdrant collection if it doesn't exist."""
    try:
        collections = client.get_collections().collections
        if collection_name not in [c.name for c in collections]:
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            logger.info(f"Created collection: {collection_name}")
        else:
            logger.info(f"Collection {collection_name} already exists")
    except Exception as e:
        logger.error(f"Error creating collection: {e}")
        raise

def index_files(
    data_dir: Path,
    collection_name: str,
    model: SentenceTransformer,
    client: QdrantClient
) -> None:
    """Index files from the data directory into Qdrant."""
    try:
        create_qdrant_collection(client, collection_name)
        
        points: List[PointStruct] = []
        supported_extensions = {".txt", ".md", ".pdf"}
        
        for file_path in data_dir.glob("*"):
            if file_path.is_file() and file_path.suffix in supported_extensions:
                text = extract_text_from_file(file_path)
                if text:
                    vector = model.encode(text)
                    points.append(
                        PointStruct(
                            id=len(points),
                            vector=vector.tolist(),
                            payload={
                                "file_name": str(file_path),
                                "file_type": file_path.suffix[1:]  # Store file type in payload
                            }
                        )
                    )
        
        if points:
            client.upsert(
                collection_name=collection_name,
                points=points
            )
            logger.info(f"Indexed {len(points)} files")
        else:
            logger.info("No files to index")
    
    except Exception as e:
        logger.error(f"Error indexing files: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Index files into Qdrant')
    parser.add_argument('--data-dir', default='/qdrant/data', help='Path to data directory')
    parser.add_argument('--collection-name', default='local-docs', help='Qdrant collection name')
    args = parser.parse_args()
    
    try:
        # Initialize components
        model = SentenceTransformer("all-MiniLM-L6-v2")
        client = QdrantClient(host="localhost", port=6333)
        
        # Create data directory if it doesn't exist
        data_dir = Path(args.data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Start indexing
        index_files(data_dir, args.collection_name, model, client)
        
    except Exception as e:
        logger.error(f"Main process failed: {e}")
        raise

if __name__ == "__main__":
    main()