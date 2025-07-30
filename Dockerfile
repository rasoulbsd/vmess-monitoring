FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

# Copy application files
COPY . .

# Make vmessping executable
RUN chmod +x vmessping

# Expose port
EXPOSE 8765

# Set environment variables
ENV SERVER_HOST=0.0.0.0
ENV SERVER_PORT=8765
ENV DEBUG=False

# Run the server with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8765", "--workers", "4", "--timeout", "120", "server.wsgi:app"] 