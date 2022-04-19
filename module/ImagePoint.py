from dataclasses import dataclass

from module.Point import Point


@dataclass
class ImagePoint:
    u: float
    v: float
    point: Point
