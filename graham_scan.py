#!/usr/bin/env python3

import math
import queue
from functools import cmp_to_key
import fileinput


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if self.x == other.x:
            return self.y <= other.y
        return self.x <= other.x

    def __le__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __repr__(self):
        return f"{self.x}\t{self.y}"


class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def angle(self):
        y_d = self.p2.y - self.p1.y
        x_d = self.p2.x - self.p1.x
        return math.atan(y_d / (x_d + 0.000000001))


def left_kink(p1, p2, p3):
    d1 = Edge(p1, p2).angle()
    d2 = Edge(p2, p3).angle()
    return d2 > d1


def right_kink(p1, p2, p3):
    return not left_kink(p1, p2, p3)


def get_hull(points, upper=True):

    def upper_cmp(p1, p2):
        if p1.x == p2.x:
            if p1.y == p2.y:
                return 0
            if p1.y > p2.y:
                return -1
            return 1
        return p1.x - p2.x

    points = sorted(points)
    p1, p2 = points[0:2]
    last = points[-1]

    rest = points[2:]
    if upper:
        rest = sorted(rest, key=cmp_to_key(upper_cmp))

    Q = queue.LifoQueue()

    Q.put(p1)
    Q.put(p2)
    for i in rest:
        q3 = i
        q2 = Q.get()
        q1 = Q.get()

        if upper:
            kink = left_kink(q1, q2, q3)
        else:
            kink = right_kink(q1, q2, q3)

        if kink:
            Q.put(q1)
            Q.put(q3)
        else:
            Q.put(q1)
            Q.put(q2)
            Q.put(q3)

        if i == last:
            break

    hull = []
    while not Q.empty():
        hull.insert(0, Q.get())

    return hull


def graham_scan(points):
    upper_hull = get_hull(points, upper=True)
    lower_hull = get_hull(points, upper=False)

    # remove duplicate start/end points
    lower_hull = lower_hull[1:-1]

    return upper_hull + lower_hull


def io_graham_scan(points_txt):
    if isinstance(points_txt, str):
        points_txt = points_txt.split('\n')
    points = []
    for line in points_txt:
        line = line.strip()
        x, y = int(line[0]), int(line[-1])
        points.append(Point(x, y))

    return '\n'.join([str(p) for p in graham_scan(points)])


if __name__ == "__main__":
    print(io_graham_scan(fileinput.input()))
