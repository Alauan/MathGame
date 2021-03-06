from typing import Union, List, Tuple
from math import sin, cos, atan2, dist, pi


def barycentre(points: Union[List, Tuple], get_round=False) -> tuple:
    if len(points) == 3:
        if get_round:
            return round((points[0][0]+points[1][0]+points[2][0])/3), round((points[0][1]+points[1][1]+points[2][1])/3)
        else:
            return (points[0][0]+points[1][0]+points[2][0])/3, (points[0][1]+points[1][1]+points[2][1])/3
    else:
        centers = []
        areas = []
        for index in range(2, len(points)):
            centers.append(barycentre([points[index], points[index-1], points[0]]))
            areas.append(area([points[index], points[index-1], points[0]]))
        while len(centers) > 1:
            k = ((areas[1] * dist(centers[0], centers[1])) /
                 (areas[0] + areas[1])) / dist(centers[0], centers[1])
            x = k * (centers[1][0] - centers[0][0]) + centers[0][0]
            y = k * (centers[1][1] - centers[0][1]) + centers[0][1]

            centers[0] = (x, y)
            areas[0] += areas[1]

            centers.pop(1)
            areas.pop(1)

        if get_round:
            return round(centers[0][0]), round(centers[0][1])
        else:
            return centers[0]


def area(ref: Union[List, Tuple]) -> int:
    ref.append(ref[0])
    s = 0
    for index in range(len(ref)-1):
        s += ref[index][0] * ref[index+1][1]
    for index in range(1, len(ref)):
        s -= ref[index][0] * ref[index-1][1]
    return abs(s) // 2


def rotate(points: Union[List, Tuple], center: Union[List, Tuple], rotation) -> List:
    rotated = []
    for index in range(len(points)):
        hip = dist(center, points[index])
        angle = atan2(points[index][1] - center[1], points[index][0] - center[0])
        angle += rotation * pi / 180
        co = round(sin(angle) * hip)
        ca = round(cos(angle) * hip)
        rotated.append((center[0] + ca, center[1] + co))
    return rotated


def is_within(points, point) -> bool:
    """ Tells if a point is within a polygon """
    odd_nodes = False
    for index in range(len(points)):
        conditions = [
            points[index][1] > point[1] > points[index - 1][1] or points[index][1] < point[1] < points[index - 1][1],
            point[0] >= points[index][0] or point[0] >= points[index - 1][0],
        ]
        if all(conditions):
            if (((points[index][0] - points[index - 1][0]) * (point[1] - points[index][1])) /
               (points[index - 1][1] - points[index][1])) > points[index][0] - point[0]:
                odd_nodes = not odd_nodes
    return odd_nodes


def resize(points, proportion):
    return [(points[0][0] + (x - points[0][0]) * proportion,
             points[0][1] + (y - points[0][1]) * proportion) for x, y in points]


def add_vectors(v1, v2):
    return [x + y for x, y in zip(v1, v2)]


def sub_vectors(v1, v2):
    return [x - y for x, y in zip(v1, v2)]
