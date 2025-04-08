import argparse
import logging
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_qdrant_connection():
    try:
        # Initialize Qdrant client
        client = QdrantClient(host="localhost", port=6333)
        
        # Check if collection exists
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        logger.info("Available collections:")
        for name in collection_names:
            logger.info(f" - {name}")
        
        if "local-docs" not in collection_names:
            logger.error("Collection 'local-docs' not found. Ingestion may have failed.")
            return
        
        # Test search functionality
        test_query = "test document"  # This is a simple test query
        logger.info(f"\nTesting search with query: '{test_query}'")
        
        # Get embeddings for the test query
        model = SentenceTransformer("all-MiniLM-L6-v2")
        query_vector = model.encode(test_query).tolist()
        
        # Perform search using query_points
        response = client.query_points(
            collection_name="local-docs",
            query=query_vector,
            limit=5
        )
        
        logger.info("\nSearch results:")
        for i, hit in enumerate(response.points, 1):
            logger.info(f"\nResult {i}:")
            logger.info(f"Score: {hit.score}")
            logger.info(f"File: {hit.payload['file_name']}")
            logger.info(f"Type: {hit.payload['file_type']}")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise

if __name__ == "__main__":
    logger.info("Testing connection to Qdrant on port 6333")
    test_qdrant_connection()