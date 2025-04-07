FROM qdrant/qdrant:latest

# Install Python and pip dependencies
RUN apt update && apt install -y python3 python3-pip curl && \
    pip install qdrant-client sentence-transformers pdfminer.six python-markdown python-dotenv

# Expose Qdrant port
EXPOSE 6333

# Run Qdrant in background and leave terminal interactive
CMD ["sh", "-c", "qdrant & bash"]