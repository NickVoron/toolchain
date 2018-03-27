#!/usr/bin/env python3

import subprocess
import contextlib
import logging
import os
import msbuild
import datetime
import PIL
import multiprocessing

from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from pathlib import Path


logging.basicConfig(level=logging.INFO)

@contextlib.contextmanager
def cwd(new_cwd):
    """Context manager for current working directory."""
    old_cwd = Path.cwd()
    logging.info('Change cwd: %s', str(new_cwd))
    os.chdir(str(new_cwd))
    yield
    logging.info('Restore cwd: %s', str(old_cwd))
    os.chdir(str(old_cwd))

def program(caption, function):
    start = datetime.datetime.now()
    function()
    stop = datetime.datetime.now()
    print(str(caption), ' finished in: ', str(stop - start))


def createImage(filename, size, function):
    im = Image.new('RGB', size)
    function(im)
    im.save(filename, "PNG")

def createImageSequence(path, basename, count, rate, size, function):
    print('create image sequence in: ', basename)
    for x in range(0, count):
       createImage(os.path.join(path, basename + str(x) + '.png'), size, lambda img: function(img, count, rate, x))

def packImageSequence(path, basename, fps):
    outputfile = str(os.path.join(path, datetime.datetime.now().strftime('(%Y_%m_%d @ %H-%M-%S)') + '(' +basename + ').avi'))
    with cwd(path):
        cmd = [
            'ffmpeg',
            '-r', 
            str(fps),
            '-i', 
            basename + r'%d.png',
            '-c:v',
            'ffv1',
            '-qscale:v',
            '0',
            outputfile
        ]
        logging.info('run ffmpeg command: %s', str(cmd))
        subprocess.check_call(cmd)
        logging.info('output: %s', str(outputfile))

def synthVideo(path, basename, frameCount, frameRate, frameSize, function):
    program('create sequence ', lambda: createImageSequence(path, basename, frameCount, frameRate, frameSize, function))
    program('encode video ',  lambda: packImageSequence(path, basename, frameRate))