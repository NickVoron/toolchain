#!/usr/bin/env python3

import subprocess
import contextlib
import logging
import os
import msbuild
from pathlib import Path
import sys

sys.path.append('toolchain/scripts/configure')
import boost_utils
import configure_boost
import configure_qt

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

root_path = Path(__file__).parent.resolve() / '..' / '..' / '..'
xcode_path = Path('_obj-lib-etc') / 'win' / 'sharedtec'
xcode_path.mkdir(parents=True, exist_ok=True)


# check boost exist
def check_boost():
    if not os.path.exists("boost-cmake/.git"):
        boost_utils.get_boost()

    if not configure_boost.check_boost_version():
        boost_utils.remove_intermediate()
        boost_utils.remove_boost()
        boost_utils.get_boost()

    pass


def build(third_party_only):
    print('third_party_only {0}'.format(third_party_only))
    with cwd(xcode_path):
        if third_party_only:
            cmd = [
                cmake_path,
                '-G', 'Visual Studio 15 2017 Win64',
                str(root_path),  # source dir
                '-DTHIRD_PARTY_ONLY=True'
            ]
            pass
        else:
            cmd = [
                cmake_path,
                '-G', 'Visual Studio 15 2017 Win64',
                str(root_path),  # source dir
                '-DTHIRD_PARTY_ONLY=False'
            ]

        logging.info('Run cmake command: %s', str(cmd))
        subprocess.check_call(cmd)
    # logging.info('Build library via Visual Studio 15 2017: ')
    # msbuild.build('sandbox.sln', 'Release', 'x64')
    pass


if __name__ == '__main__':
    # build script
    configure_qt.configure(False)
    check_boost()
    build(False)
