# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PORT=8000
ENV DEBUG=True

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        pkg-config \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/static /app/media /app/staticfiles /app/css /app/js /app/assets

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Set DEBUG=False for production runtime
ENV DEBUG=False

# Set permissions
RUN chmod +x /app/manage.py

# Expose port
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/ || exit 1

# Default command - migrate and start server
CMD python manage.py migrate && gunicorn --bind 0.0.0.0:$PORT bank_challan.wsgi:application

