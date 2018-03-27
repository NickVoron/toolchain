#!/usr/bin/env python3

import video
import rasterizer

def points(count, pointFunction):
    result = []
    for i in range(0, count):
        result.append(pointFunction(i))
    return result

def pointFunction(index, frameIndex):
    return ((frameIndex / ((index + 1) / 10.0 )), 100.5 + 30 * index)

def frameFunction(image, count, rate, index):
    for pt in points(30, lambda pt: pointFunction(pt, index)):
        rasterizer.point(image, pt, 5, (1.0, 1.0, 1.0))

video.synthVideo('d:/synth/', 'frame', 600, 60, (1024, 1024), frameFunction)