FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for pandas/openpyxl if needed
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables
ENV DATABASE_URL=sqlite:///./data/tasks.db
ENV PORT=8000

# Create data directory for volume mounting
RUN mkdir -p /app/data

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
