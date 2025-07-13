FROM python:3.10-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including ffmpeg and libsndfile1
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and related folders
COPY app.py .
COPY templates ./templates
COPY static ./static

# Create audio folder for uploads and outputs
RUN mkdir -p audio

# Expose Flask's default port
EXPOSE 5000

# Start the Flask app
CMD ["python", "app.py"]
