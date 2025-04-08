# Qdrant DevContainer for File Embeddings

This project provides a development container setup for running Qdrant with file embeddings. It includes everything needed to index and search text documents using vector similarity search.

## Prerequisites

1. Docker Desktop must be running before starting the devcontainer
2. VS Code with the Remote - Containers extension
3. Internet connection (for downloading dependencies)

## Getting Started

1. Ensure Docker Desktop is running on your system
2. Open this folder in VS Code
3. Click the green "Reopen in Container" button in the bottom right corner
   - Or press `F1` and type "Dev Containers: Reopen in Container"

## Project Structure
qdrant_server_devcontainer/ ├── .devcontainer/ │ ├── devcontainer.json │ └── Dockerfile ├── requirements.txt ├── ingest.py └── data/ # Place your text files here


## Usage

1. Place your text files in the `data/` directory
2. The container will automatically start Qdrant
3. After the container is built You should be able to access Qdrant at `http://localhost:6333`
4. Run the ingestion script manually from within the container:
   ```bash
   python ingest.py
   ```

## Features

- Qdrant vector database running in the background
- Automatic file indexing using sentence-transformers
- Python environment with all necessary dependencies
- VS Code Python extension pre-installed

## Technical Details

- Qdrant runs on a dynamically assigned port (check the output panel after container build)
- Uses `all-MiniLM-L6-v2` for text embeddings
- Creates a collection named "local-docs" with cosine similarity
- Supports text files (.txt), markdown files (.md), and PDF files (.pdf) in the data directory

## Troubleshooting

1. If the container fails to start:
   - Ensure Docker Desktop is running
   - Check that no other process is using the dynamically assigned port
   - Verify all dependencies are properly installed

2. If files aren't being indexed:
   - Check that files are in the `data/` directory
   - Verify file extensions are supported (currently .txt, .md, .pdf)
   - Ensure files are readable by the container

## License

MIT License

## TODO
- handle giant PDFs efficiently,
- extract text per page using parallel processing,
- embed and push each chunk as it’s ready,
- support GPU embedding if torch.cuda.is_available()?
- add support for epub files