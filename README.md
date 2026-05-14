# taubenturret-backend

An object detection backend for the [TaubenTurret system](https://github.com/MLWeber/taubenturret), utilizing YOLO and OpenVINO for high-speed inference.

## Features
* **FastAPI & Uvicorn:** Provides a high-performance REST API to handle inference requests.
* **YOLO & OpenVINO:** Leverages hardware-agnostic, heavily optimized INT8 object detection for fast CPU processing.
* **Image Collection:** Automatically saves incoming detections, allowing you to manually categorize true/false positives for future custom model calibration.
* **Docker Ready:** Easily build and deploy the backend as a lightweight, platform-independent container.

## System Requirements
* Python 3.10+
* `make` and `uv` for environment management and building.
* (If running locally without Docker) `libgl1` and `libglib2.0-0` for OpenCV support.

## Configuration
By default, the backend will listen on port `8080` and save images to a local `./images` directory. If you need to change these paths, you can modify them directly within the `docker-compose.yml` file.

## Installation
Use the provided `Makefile` to quickly set up the environment and install dependencies:
```bash
make install
```
Before starting the application, you must export the raw YOLO weights into the highly optimized OpenVINO format:
```bash
make model
```

## Usage
Start the local backend server by running:
```bash
make run
```

### Docker Deployment
To build and run the production-ready Docker image:
```bash
make docker
docker run -d -p 8080:8080 taubenturret-backend:latest
```

Once running, the API will accept POST requests on `/v1/detect/bird` with an attached image file.
