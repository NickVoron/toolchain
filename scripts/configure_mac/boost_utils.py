import utils
import shutil
import os
import subprocess
from pathlib import Path
import logging
import multiprocessing

boost_cmake_path = 'boost-cmake'


def remove_boost():
    print("remove boost:")

    if os.path.exists(boost_cmake_path):
        shutil.rmtree(boost_cmake_path, onerror=utils.del_rw)

    print("complete")
    pass


def remove_intermediate():
    print("remove obj_lib_etc:")

    if os.path.exists(utils.obj_lib_etc_path):
        shutil.rmtree(utils.obj_lib_etc_path, onerror=utils.del_rw)
    print("complete")
    pass


def get_boost():
    print("get boost")
    if os.path.exists(".git"):
        # create submodule for git repo
        with utils.cwd('.'):
            subprocess.call(['git', 'submodule', 'update', '--init', '--recursive'])
    elif os.path.exists(".hg"):
        # check if boost always exist
        subprocess.call([r'git', r'clone', 'https://github.com/nvoronetskiy/boost-cmake.git'])
    print("complete")
    pass


def run_boost_cmake():
    root_path = Path('../../../../') / boost_cmake_path
    build_path = Path(utils.obj_lib_etc_path) / utils.platform / utils.sharedtec / boost_cmake_path
    build_path.mkdir(parents=True, exist_ok=True)
    with utils.cwd(build_path):
        cmd = [
            utils.cmake_path,
            '-G', 'Visual Studio 15 2017 Win64',
            str(root_path)  # source dir
        ]
        logging.info('Run cmake command: %s', str(cmd))
        subprocess.check_call(cmd)
    pass


def get_boost_sorce_sub_path():
    sub_path = boost_cmake_path + '/boost'
    un_existing_path = 'eddd8278-b56a-4f35-a399-40eefbd6b5da'

    if os.path.exists(sub_path):
        dillist = os.listdir(sub_path)
        if len(dillist)>1:
            print("boost source folder({0}) contain more that one subfolder, script can't understand where look src".format(sub_path))
            print('run configure with clear flags( configure.py --boost-clear )')
            exit()

        if len(dillist) == 0:
            # if boost folder not exitst we return unxisting path
            return un_existing_path

        return sub_path + '/' + dillist[0]

    return un_existing_path


# check is boost libs exist, return True if boost libs exist
def check_boost_libs_exist():
    boost_build_path = Path(get_boost_sorce_sub_path()) / 'stage' / 'x64' / 'lib'

    filesystem_lib_exist = False
    unittest_lib_exist = False
    if boost_build_path.exists():
        for child in boost_build_path.iterdir():

            if child.name.find('libboost_filesystem') != -1:
                filesystem_lib_exist = True

            if child.name.find('libboost_unit_test_framework') != -1:
                unittest_lib_exist = True

        pass

    return filesystem_lib_exist and unittest_lib_exist


def boost_build():
    boost_dir = get_boost_sorce_sub_path()

    if os.path.exists(boost_dir):
        with utils.cwd(boost_dir):
            if not os.path.exists("bjam.exe") and os.path.exists("bootstrap.bat"):
                # build bootstrap
                vs_console = utils.find_vs()
                bat_file_path = 'build.bat'

                bootstrap = os.getcwd() + '\\bootstrap.bat'
                print(bootstrap)

                bat_file = open(bat_file_path, 'w')
                bat_file.write('@echo off\n')
                bat_file.write('call \"' + vs_console + '\"\n')
                bat_file.write('cd ' + os.getcwd() + '\n')
                bat_file.write('call ' + bootstrap + '\n')
                bat_file.close()

                cmd = 'cmd /C '
                cmd += bat_file_path
                p1 = subprocess.Popen(cmd)
                p1.wait()

            if os.path.exists("bjam.exe"):
                # build boost
                jobs_count = '-j' + str(multiprocessing.cpu_count())
                subprocess.call([r'bjam', r'--stagedir=stage/x64', jobs_count, r'toolset=msvc', r'address-model=64',
                                     r'variant=release', r'threading=multi', r'link=static',
                                     r'runtime-link=static,shared', r'define=_SECURE_SCL=0',
                                     r'define=_HAS_ITERATOR_DEBUGGING=0', r'define=BOOST_TEST_NO_MAIN'])
                subprocess.call([r'bjam', r'--stagedir=stage/x64', jobs_count, r'toolset=msvc', r'address-model=64',
                                     r'variant=debug', r'threading=multi', r'link=static',
                                     r'runtime-link=static,shared', r'define=BOOST_TEST_NO_MAIN'])
            else:
                print("bjam not found")
    pass
