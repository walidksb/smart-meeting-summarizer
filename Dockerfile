# Use official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies (ffmpeg + build essentials)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files first (better layer caching)
COPY requirements.txt dev-requirements.txt ./

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt -r dev-requirements.txt

# Copy the project code
COPY . .

# Set PYTHONPATH so src/ can be imported correctly
ENV PYTHONPATH=/app

# Define default command (adjust based on your project entrypoint)
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
