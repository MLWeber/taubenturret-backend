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

import datetime
import io
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError

from taubenturret_backend import config
from taubenturret_backend.detector import UnsupportedClassError

router = APIRouter()


@router.get("/ping")
def ping() -> str:
    return "pong"


@router.get("/classes")
def get_classes(request: Request) -> JSONResponse:
    detector = request.app.state.detector
    return JSONResponse(content={"success": True, "classes": list(detector.class_name_to_id.keys())})


@router.post("/detect")
@router.post("/detect/{classes}")
async def detect_objects(
    request: Request, image: Annotated[UploadFile, File(...)], classes: str | None = None
) -> JSONResponse:
    contents = await image.read()

    try:
        img = Image.open(io.BytesIO(contents))
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Invalid or corrupted image file") from None

    class_list = [c.strip() for c in classes.split(",") if c.strip()] if classes else None

    detector = request.app.state.detector
    try:
        detections = detector.analyze(img, classes=class_list)
    except UnsupportedClassError as e:
        raise HTTPException(status_code=400, detail=str(e)) from None

    if config.SAVE_IMAGES == "all" or (config.SAVE_IMAGES == "detection" and len(detections) > 0):
        # save image so we can use the false positives as training data later
        suffix = "_detected" if len(detections) > 0 else "_none"
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat().replace(":", "-")
        img.save(config.IMAGES_DIR / "new" / f"{timestamp}{suffix}.jpg")

    return JSONResponse(content={"success": True, "detections": detections})
