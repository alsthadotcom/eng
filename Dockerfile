# Use Python 3.11 image
FROM python:3.11-slim

# Set working directory to /app
WORKDIR /app

# Copy the backend requirements first for caching
COPY backend/requirements.txt /app/backend/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy the entire project
COPY . /app

# Expose the default port (Railway will override this with $PORT)
EXPOSE 8000

# Start the application from the backend directory
# We use the module path 'main:app' and set the PYTHONPATH to include common folders
WORKDIR /app/backend
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
