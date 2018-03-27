import utils
import getopt
import sys
import os
import subprocess
import shutil

toolchain_path = 'toolchain'
qt_binaries_path = 'toolchain/qt'
qmake_path = 'toolchain/qt/bin/qmake.exe'
qt_repo_address = 'https://strelok_ndv@bitbucket.org/strelok_ndv/qt5.10.git'
qt_repo_paths = ['toolchain/qt5.10']    # when fix script to update new qt version add to this array new qt path
unpack_arc_cmd = ['toolchain/7z/7za.exe', 'x', 'toolchain/qt5.10/msvc2017_64.7z', '-otoolchain/qt', '-pd04a6e89']


def get_qt_repo():
    print("get qt")
    if os.path.exists(".git"):
        # create submodule for git repo
        with utils.cwd(toolchain_path):
            subprocess.call(['git', 'submodule', 'update', '--init', '--recursive'])
        pass
    elif os.path.exists(".hg"):
        with utils.cwd(toolchain_path):
            subprocess.call([r'git', r'clone', r'--progress', qt_repo_address])
        pass
    print("complete")

    pass


def remove_qt_repo():
    for qt_repo_path in qt_repo_paths:
        print("try remove qt repo ({0}):".format(qt_repo_path))
        if os.path.exists(qt_repo_path):
            shutil.rmtree(qt_repo_path, onerror=utils.del_rw)
        print("complete")
        pass
    pass


def remove_qt_binaries():
    print('remove qt binaries:')
    if os.path.exists(qt_binaries_path):
        shutil.rmtree(qt_binaries_path, onerror=utils.del_rw)
    print('complete')
    pass


def unpack_repo():
    print("unpack archive wait...:")
    unpack_process = subprocess.Popen(unpack_arc_cmd)
    unpack_process.wait()
    print('complete')
    pass


def configure(force_clear):

    if not os.path.exists(qmake_path) or force_clear:
        print("clear qt artifacts:")
        remove_qt_repo()
        remove_qt_binaries()
        print('clear complete')
        get_qt_repo()
        unpack_repo()
        remove_qt_repo()
        print('all complete')
        pass
    else:
        print('qt check complete, qmake exist')
    pass


def setup():
    input_args = sys.argv[1:]   # skip first param - path to python file
    optlist, args = getopt.getopt(input_args, '', ['force'])

    force_clear = False

    for opt_type, value in optlist:
        if opt_type == "--force":
            force_clear = True
            pass
        pass

    configure(force_clear)
    pass


if __name__ == '__main__':
    setup()
