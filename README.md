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
By default, the backend will listen on port `8081` and save images to a local `./images` directory. If you need to change these paths, you can modify them directly within the `docker-compose.yml` file.

## Installation
Use the provided `Makefile` to quickly set up the environment and install dependencies:
```bash
make install
```
Before starting the application, you must export the raw YOLO weights into the highly optimized OpenVINO format:
```bash
make model
```
Note that this will download the full COCO dataset which can take a lot of time and disk space. If you accept slightly lower accuracy, you can use the much smaller COCO128 dataset, by running `make model DATASET=coco128.yaml` instead.

## Usage
Start the local backend server by running:
```bash
make run
```

### Docker Deployment
Build and run the image:
```bash
make docker
docker run -d -p 8081:8081 -v ./images:/app/images taubenturret-backend:latest
```

Or use docker-compose:
```bash
docker compose up -d
```

Once running, the API will accept POST requests on `/v1/detect/bird` with an attached image file.
