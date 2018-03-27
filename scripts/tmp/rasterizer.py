#!/usr/bin/env python3

import math

def section(h, r = 1): #returns the positive root of intersection of line y = h with circle centered at the origin and radius r
    #assert(r >= 0) #assume r is positive, leads to some simplifications in the formula below (can factor out r from the square root)
    if (h < r): 
        return math.sqrt(r * r - h * h) 
    else: 
        return 0 #http://www.wolframalpha.com/input/?i=r+*+sin%28acos%28x+%2F+r%29%29+%3D+h

def g(x, h, r = 1): #indefinite integral of circle segment
    return .5 * (math.sqrt(1 - x * x / (r * r)) * x * r + r * r * math.asin(x / r) - 2 * h * x) #http://www.wolframalpha.com/input/?i=r+*+sin%28acos%28x+%2F+r%29%29+-+h

def area_4(x0, x1, h, r): #area of intersection of an infinitely tall box with left edge at x0, right edge at x1, bottom edge at h and top edge at infinity, with circle centered at the origin with radius r
    if(x0 > x1):
        x0, x1 = x1, x0 #this must be sorted otherwise we get negative area
    s = section(h, r)
    return g(max(-s, min(s, x1)), h, r) - g(max(-s, min(s, x0)), h, r) #integrate the area

def area_5(x0, x1, y0, y1, r): #area of the intersection of a finite box with a circle centered at the origin with radius r
    if(y0 > y1):
        y0, y1 = y1, y0 #this will simplify the reasoning

    if(y0 < 0):
        if(y1 < 0):
            return area_5(x0, x1, -y0, -y1, r) #the box is completely under, just flip it above and try again
        else:
            return area_5(x0, x1, 0, -y0, r) + area_5(x0, x1, 0, y1, r) #the box is both above and below, divide it to two boxes and go again
    else:
        #assert(y1 >= 0) #y0 >= 0, which means that y1 >= 0 also (y1 >= y0) because of the swap at the beginning
        return area_4(x0, x1, y0, r) - area_4(x0, x1, y1, r) #area of the lower box minus area of the higher box


def area(x0, x1, y0, y1, cx, cy, r): #area of the intersection of a general box with a general circle
    x0 -= cx 
    x1 -= cx
    y0 -= cy 
    y1 -= cy
    #get rid of the circle center
    return area_5(x0, x1, y0, y1, r)

def set_pixel_native(image, pixel, value):
    if pixel[0] >= 0 and pixel[1] >= 0 and pixel[0] < image.size[0] and pixel[1] < image.size[1]:
        color = ( int(value[0] * 255.0), int(value[1] * 255.0), int(value[2] * 255.0) )
        image.putpixel(pixel, color)

def point(image, pixel, radius, value):
    x0 = pixel[0]
    y0 = pixel[1]

    xi = int(x0)
    yi = int(y0)
    for yy in range(yi - int(radius + 0.5) - 1, yi + int(radius + 0.5) + 1):
        for xx in range(xi - int(radius + 0.5) - 1, xi + int(radius + 0.5) + 1):
            coverage = area(xx, xx+1, yy, yy+1, x0, y0, radius)
            set_pixel_native(image, (xx, yy), (value[0] * coverage, value[1] * coverage, value[2] * coverage))