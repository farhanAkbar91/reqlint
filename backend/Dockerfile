FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc g++ git && rm -rf /var/lib/apt/lists/*

# Copy backend & ai-engine dependencies
COPY backend/requirements.txt /app/requirements.txt
COPY ai-engine/requirements-ai.txt /app/requirements-ai.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-ai.txt

# Copy source code
COPY backend /app/backend
COPY ai-engine /app/ai-engine

WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
