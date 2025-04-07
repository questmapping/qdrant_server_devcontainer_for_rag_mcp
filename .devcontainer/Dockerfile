FROM qdrant/qdrant:latest

# Install system dependencies + supervisor
RUN apt update && apt install -y python3 python3-pip python3-venv curl procps supervisor

# Set up app and virtualenv
RUN mkdir -p /app /var/log/supervisor && python3 -m venv /app/venv

# Install Python packages
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN /app/venv/bin/pip install --upgrade pip && /app/venv/bin/pip install -r requirements.txt

# Add venv activation to .bashrc
RUN echo "source /app/venv/bin/activate" >> /root/.bashrc

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 6333

# Run Supervisor as PID 1
CMD ["/usr/bin/supervisord", "-n"]