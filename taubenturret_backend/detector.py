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
from typing import Any

from PIL import Image
from ultralytics import YOLO

logger = logging.getLogger(__name__)


class UnsupportedClassError(Exception):
    """Exception raised when a requested class is not supported by the model."""


class Detector:
    def __init__(self, model: str) -> None:
        self.model = YOLO(model, task="detect")

        # Map class names to their IDs dynamically using the loaded model
        self.class_name_to_id = {name: class_id for class_id, name in self.model.names.items()}

    def analyze(self, img: Image.Image, classes: list[str] | None = None) -> list[dict[str, Any]]:
        included_classes = None
        if classes is not None:
            included_classes = []
            for cls in classes:
                if cls not in self.class_name_to_id:
                    msg = f"Class '{cls}' not recognized by the object detection model."
                    raise UnsupportedClassError(msg)
                included_classes.append(self.class_name_to_id[cls])

        result = self.model(img, classes=included_classes, verbose=False)[0]

        logger.debug(f"Found {len(result)} object(s):")
        detections = []
        if len(result) > 0:
            logger.debug(result.summary())

        for obj in result.summary():
            box = obj["box"]
            xc = round((box["x1"] + box["x2"]) / 2)
            yc = round((box["y1"] + box["y2"]) / 2)

            logger.debug(f"Detection at x={xc}, y={yc}!")
            detections.append({
                "class": obj["name"],
                "x1": box["x1"],
                "x2": box["x2"],
                "y1": box["y1"],
                "y2": box["y2"],
            })
        return detections
