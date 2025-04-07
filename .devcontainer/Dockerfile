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

# Switch to the qdrant directory where entrypoint.sh and the qdrant binary reside
WORKDIR /qdrant

# Ensure entrypoint.sh is executable
RUN chmod +x entrypoint.sh

# Expose Qdrant ports (HTTP and gRPC)
EXPOSE 6333 6334

# # Run Supervisor as PID 1
# CMD ["/usr/bin/supervisord", "-n"]

# Use a shell command to change to /qdrant and run the entrypoint script
ENTRYPOINT ["/bin/sh", "-c", "./entrypoint.sh"]

# By default, this will start Qdrant with the entrypoint. You can still enter the shell interactively.