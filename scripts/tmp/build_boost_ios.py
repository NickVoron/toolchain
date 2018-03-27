#!/usr/bin/env python3

import subprocess
import contextlib
import logging
import os

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

root_path = Path(__file__).parent.resolve()
boost_path = root_path  / 'boost-cmake'

xcode_path = Path(os.environ['SharedTecINT']) / 'xcode' / 'boost'
xcode_path.mkdir(parents=True, exist_ok=True)

with cwd(xcode_path):
    cmd = [
        'cmake',
        '-G', 'Xcode',
        '-DCMAKE_TOOLCHAIN_FILE=%s' % str(root_path / 'toolchain' / 'ios.cmake'),
        str(boost_path) # source dir
    ]

    logging.info('Run cmake command: %s', str(cmd))

    subprocess.check_call(cmd)

    logging.info('Build library via xcodebuild: ')

    subprocess.check_call(['xcodebuild', '-target', 'ALL_BUILD', '-configuration', 'Debug'])
