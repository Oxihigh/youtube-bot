# Use lightweight Python 3.11 slim image
FROM python:3.11-slim

# Prevent interactive prompts and configure unbuffered output
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies including FFmpeg with libass support and fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libass-dev \
    fonts-liberation \
    fonts-dejavu-core \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency definition
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure output and temp directories exist
RUN mkdir -p output temp assets/music assets/fonts

# Expose Web Dashboard port
EXPOSE 8000

# Default command runs the web server and background pipeline
CMD ["python", "main.py", "--port", "8000"]
