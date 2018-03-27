import os
import contextlib
from pathlib import Path
import logging
import stat
import subprocess


obj_lib_etc_path = '_obj-lib-etc'
boost_cmake_path = 'boost-cmake'
sharedtec = 'sharedtec'
platform = 'windows'
cmake_path = os.path.abspath('toolchain/cmake/bin/cmake.exe')


# смена локальной папки скрипта
@contextlib.contextmanager
def cwd(new_cwd):
    """Context manager for current working directory."""
    old_cwd = Path.cwd()
    logging.info('Change cwd: %s', str(new_cwd))
    os.chdir(str(new_cwd))
    yield
    logging.info('Restore cwd: %s', str(old_cwd))
    os.chdir(str(old_cwd))
    pass


# смена на чтение файла, убираня флага readonly
def del_rw(action, name, exc):
    print("    remove read only file: {0}", name)
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)
    pass


def check_repo_version(repo_path, repo_address):
    with cwd(repo_path):
        print("boost exist, try to update:")
        p = subprocess.Popen(['git', 'rev-parse', 'HEAD'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.stdin.close()
        current_revision = p.stdout.read().decode("utf-8")
        current_revision = current_revision[: len(current_revision) - 1]

        git = subprocess.Popen(['git', 'ls-remote', repo_address],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        git.stdin.close()
        remote_revision = git.stdout.read().decode("utf-8")
        found = remote_revision.find("HEAD")
        remote_revision = remote_revision[:found - 1]

        print('   local head:  {0}'.format(current_revision))
        print('   remove head: {0}'.format(remote_revision))

        return current_revision == remote_revision
    pass


def find_vs():
    possible_variants = [
        r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\Common7\Tools\VsDevCmd.bat",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat",
        r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\Common7\Tools\VsDevCmd.bat"]
    for target in possible_variants:
        if os.path.exists(target):
            return target
    return r"vcvars64.bat"


def replce_cmakefile(file_to_search, text_to_search, text_to_replace):
    file_data = ''
    with open(file_to_search, 'r') as file:
        file_data = file.read()

    file_data = file_data.replace(text_to_search, text_to_replace)

    with open(file_to_search, 'w') as file:
        file.write(file_data)

    pass




