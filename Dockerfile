# Use the official Python base image for AMD64
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-6 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY static .
COPY templates .
COPY model.py .
COPY malaria_model.h5 .
COPY app.py .

# Expose port (adjust if needed for FastAPI or other framework)
EXPOSE 8000

# Define the command to run the application
CMD ["fastapi", "run", "app.py", "--port", "8000"]
