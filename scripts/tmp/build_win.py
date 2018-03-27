#!/usr/bin/env python3

import subprocess
import contextlib
import logging
import os
import msbuild
from pathlib import Path

#
# Logger
#

logging.basicConfig(level=logging.INFO)

#
# Helpers
#

@contextlib.contextmanager
def cwd(new_cwd):
    """Context manager for current working directory."""
    old_cwd = Path.cwd()
    logging.info('Change cwd: %s', str(new_cwd))
    os.chdir(str(new_cwd))
    yield
    logging.info('Restore cwd: %s', str(old_cwd))
    os.chdir(str(old_cwd))

#
# Work
#

cmake_path = os.path.abspath('toolchain/cmake/bin/cmake.exe')
print(cmake_path)

root_path = Path(__file__).parent.resolve()
xcode_path = Path('_obj-lib-etc') / 'win' / 'sharedtec'
xcode_path.mkdir(parents=True, exist_ok=True)

with cwd(xcode_path):
    cmd = [
        cmake_path,
        '-G', 'Visual Studio 15 2017 Win64',
        str(root_path) # source dir
    ]

    logging.info('Run cmake command: %s', str(cmd))
    subprocess.check_call(cmd)

    # logging.info('Build library via Visual Studio 15 2017: ')
    # msbuild.build('sandbox.sln', 'Release', 'x64')