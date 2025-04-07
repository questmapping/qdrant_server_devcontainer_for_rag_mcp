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

# # Copy supervisor config
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Ensure entrypoint.sh can be executed (qdrant has its own entrypoint)
RUN chmod +x /qdrant/entrypoint.sh

EXPOSE 6333

# # Run Supervisor as PID 1
# CMD ["/usr/bin/supervisord", "-n"]

# Set entrypoint to run entrypoint.sh (starting Qdrant)
ENTRYPOINT ["/qdrant/entrypoint.sh"]

# By default, this will start Qdrant with the entrypoint. You can still enter the shell interactively.