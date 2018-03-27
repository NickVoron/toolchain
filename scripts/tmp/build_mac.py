#!/usr/bin/env python3

import subprocess
import contextlib
import logging
import os
import msbuild
from pathlib import Path
# 
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

cmake_path = 'cmake'

root_path = Path(__file__).parent.resolve()
xcode_path = Path('_obj-lib-etc') / 'mac' / 'sharedtec'
xcode_path.mkdir(parents=True, exist_ok=True)

 # cmake -DOPENSSL_ROOT_DIR=/usr/local/Cellar/openssl/1.0.2n -DOPENSSL_LIBRARIES=/usr/local/Cellar/openssl/1.0.2n/lib -G Xcode ../../..

with cwd(xcode_path):
    cmd = [
        cmake_path,
        '-G', 'Xcode',
        str(root_path) # source dir
    ]

    logging.info('Run cmake command: %s', str(cmd))
    subprocess.check_call(cmd)

    logging.info('Build library via Xcode: ')
    subprocess.check_call(['xcodebuild', '-target', 'ALL_BUILD', '-configuration', 'Debug'])
