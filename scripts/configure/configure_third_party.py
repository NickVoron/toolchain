import utils
import getopt
import sys
import os
import subprocess
import shutil
import sys

sys.path.append('toolchain/scripts/build')
import build_win


def setup():
    print('run third party build')
    build_win.build(True)
    pass


if __name__ == '__main__':
    setup()
