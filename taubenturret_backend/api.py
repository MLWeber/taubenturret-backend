# taubenturret - An automated, computer vision driven water turret system.
# Copyright (C) 2026 Michael Weber
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from taubenturret_backend import config
from taubenturret_backend.detector import Detector
from taubenturret_backend.routes import router

API_PREFIX = "/v1"

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL, logging.INFO),
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),
        ],
        force=True,
    )

    # Direct FastAPI and Uvicorn logs to the root logger
    for logger_name in ("fastapi", "uvicorn", "uvicorn.access", "uvicorn.error"):
        req_logger = logging.getLogger(logger_name)
        req_logger.handlers.clear()
        req_logger.propagate = True

    if config.SAVE_IMAGES in ["detection", "all"]:
        for subdir in ["new", "true-positives", "false-positives"]:
            target_dir = config.IMAGES_DIR / subdir
            if not target_dir.exists():
                target_dir.mkdir(parents=True, exist_ok=True)
            elif not target_dir.is_dir():
                msg = f"Cannot create directory {target_dir}: File exists and is not a directory."
                raise RuntimeError(msg)
    elif config.SAVE_IMAGES != "no":
        logger.warning(f"Invalid configuration SAVE_IMAGES={config.SAVE_IMAGES}. Must be 'no', 'detection', or 'all'.")

    detectors = {"bird": Detector([14], model="yolo_openvino_model")}
    app.state.detectors = detectors

    yield
    # Shutdown


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router, prefix=API_PREFIX)
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
