FROM python:3.10-slim

WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files (including templates/ and static/)
COPY . .

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
