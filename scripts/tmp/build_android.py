#!/usr/bin/env python3

import subprocess
import contextlib
import logging
import os
import shutil

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
intermediateENV = os.environ['SharedTecINT']
if len(intermediateENV) > 0:
    intermediate_path = intermediateENV
else 
    intermediate_path = '_obj-lib-etc'

root_path = Path(__file__).parent.resolve()
build_path = Path(intermediate_path) / 'android' / 'sharedtec'
build_path.mkdir(parents=True, exist_ok=True)

with cwd(build_path):
    # See for options help: https://developer.android.com/ndk/guides/cmake.html
    # shutil.rmtree(root_path / 'build')
    cmd = [
        'cmake',
        '-G', 'Ninja',
        '-DCMAKE_TOOLCHAIN_FILE=%s' % str(Path('toolchain') / 'ndk-bundle' / 'build' / 'cmake' / 'android.toolchain.cmake'),
        '-DANDROID_TOOLCHAIN=clang',
        '-DANDROID_ABI=arm64-v8a',
        '-DANDROID_PLATFORM=android-21',
        '-DANDROID_STL=gnustl_static',
        '-DANDROID_CPP_FEATURES=rtti exceptions',
        '-DCMAKE_BUILD_TYPE=Release',
        str(root_path) # source dir
    ]

    logging.info('Run cmake command: %s', str(cmd))

    subprocess.check_call(cmd)

    cmd_build = ['cmake', '--build', '.', '--', '-j', '8']

    logging.info('Build library via ninja: %s', str(cmd_build))

    subprocess.check_call(cmd_build)

print('OK')