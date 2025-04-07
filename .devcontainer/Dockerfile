FROM qdrant/qdrant:latest

# Install system dependencies
RUN apt update && apt install -y python3 python3-pip python3-venv curl procps

# Create app directory and virtual environment
RUN mkdir -p /app && python3 -m venv /app/venv

# Copy requirements.txt and install packages in virtual environment
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN /app/venv/bin/pip install --upgrade pip && /app/venv/bin/pip install -r requirements.txt

# Activate virtual environment
RUN echo "source /app/venv/bin/activate" >> /root/.bashrc

# Expose Qdrant port
EXPOSE 6333

# Run Qdrant in background and leave terminal interactive
CMD ["sh", "-c", "qdrant & bash"]