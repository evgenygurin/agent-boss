FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for persistence
RUN mkdir -p /app/pagelogs /app/boss_teachability_db /app/boss_mem0_storage /app/boss_chroma_db /app/logs

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "ultimate_boss_with_memory.py"]
