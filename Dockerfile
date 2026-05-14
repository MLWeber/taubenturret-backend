FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for OpenCV and OpenVINO
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY pyproject.toml .
COPY README.md .
RUN pip install --no-cache-dir .

# Copy application code
COPY taubenturret_backend/ ./taubenturret_backend/
COPY yolo_openvino_model/ ./yolo_openvino_model/

# Set environment variables
ENV API_HOST=0.0.0.0
ENV API_PORT=8080

EXPOSE 8080
CMD ["sh", "-c", "exec uvicorn taubenturret_backend.api:create_app --host $API_HOST --port $API_PORT --factory"]
