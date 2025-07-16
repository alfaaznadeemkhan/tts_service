FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    libespeak1 \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

EXPOSE 5050

CMD ["python", "app.py"]
