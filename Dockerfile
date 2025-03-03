FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and model files
COPY main.py .
COPY deploy.prototxt.txt .
COPY res10_300x300_ssd_iter_140000.caffemodel .

# Set display environment variable
ENV DISPLAY=:0

CMD ["python", "main.py"]