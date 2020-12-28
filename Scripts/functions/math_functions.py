from typing import Union, List, Tuple
from math import sqrt


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
            k = ((areas[1] * distance(centers[0], centers[1])) /
                 (areas[0] + areas[1])) / distance(centers[0], centers[1])
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


def area(points: Union[List, Tuple]) -> int:
    ref = points
    ref.append(points[0])
    s = 0
    for index in range(len(ref)-1):
        s += ref[index][0] * ref[index+1][1]
    for index in range(1, len(ref)):
        s -= ref[index][0] * ref[index-1][1]
    return abs(s) // 2


def distance(p1, p2):
    return sqrt(abs(p1[0]-p2[0])**2 + abs(p1[1]-p2[1])**2)

