import subprocess
import logging
import os
import sys
import getopt
import utils
import boost_utils

logging.basicConfig(level=logging.INFO)
cmake_path = os.path.abspath('toolchain/cmake/bin/cmake.exe')


# return true is local revision is equal remote
def check_boost_version():
    with utils.cwd(utils.boost_cmake_path):
        print("boost exist, try to update:")
        p = subprocess.Popen(['git', 'rev-parse', 'HEAD'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        p.stdin.close()
        current_revision = p.stdout.read().decode("utf-8")
        current_revision = current_revision[: len(current_revision) - 1]

        git = subprocess.Popen(['git', 'ls-remote', 'https://github.com/nvoronetskiy/boost-cmake.git'],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        git.stdin.close()
        remote_revision = git.stdout.read().decode("utf-8")
        found = remote_revision.find("HEAD")
        remote_revision = remote_revision[:found - 1]

        print('   local head:  {0}'.format(current_revision))
        print('   remove head: {0}'.format(remote_revision))

        return current_revision == remote_revision
    pass


def check_and_update_boost(force_clear_boost, force_build_boost):

    if not os.path.exists("boost-cmake/.git"):
        boost_utils.get_boost()

    if not check_boost_version() or force_clear_boost:
    #     if force_clear_boost:
    #         print("force boost clear")
    #     else:
    #         print('revision NOT equal, try update')
    #
    #     boost_utils.remove_intermediate()
    #     boost_utils.remove_boost()
    #     boost_utils.get_boost()
        pass
    else:
    #     print('complete: revision equal, update not required')
    #
    # if not boost_utils.check_boost_libs_exist() or force_build_boost:
    #     print("start boost cmake")
    #     boost_utils.run_boost_cmake()
    #     boost_utils.boost_build()
        pass
    pass


def setup():
    input_args = sys.argv[1:]   # skip first param - path to python file
    optlist, args = getopt.getopt(input_args, '', ['boost-clear', 'boost-build'])

    force_clear_boost = False
    force_build_boost = False

    for opt_type, value in optlist:
        if opt_type == "--boost-clear":
            force_clear_boost = True
            pass
        if opt_type == "--boost-build":
            force_build_boost = True
            pass
        pass

    check_and_update_boost(force_clear_boost, force_build_boost)
    pass


if __name__ == '__main__':
    setup()
