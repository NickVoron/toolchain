#!/usr/bin/env python3

import subprocess, contextlib, logging, os, shutil, msbuild
import multiprocessing
from pathlib import Path

logging.basicConfig(level=logging.INFO)

@contextlib.contextmanager
def cwd(new_cwd):
    """Context manager for current working directory."""
    old_cwd = Path.cwd()
    logging.info('Change cwd: %s', str(new_cwd))
    os.chdir(str(new_cwd))
    yield
    logging.info('Restore cwd: %s', str(old_cwd))
    os.chdir(str(old_cwd))

def mergeTree(sourceRoot, destRoot, overwrite = True):
    if not os.path.exists(destRoot):
        return False
    ok = True
    for path, dirs, files in os.walk(sourceRoot):
        relPath = os.path.relpath(path, sourceRoot)
        destPath = os.path.join(destRoot, relPath)
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        for file in files:
            destFile = os.path.join(destPath, file)
            if not overwrite and os.path.isfile(destFile):
                print("Skipping existing file:", os.path.join(relPath, file))
                ok = False
                continue
            srcFile = os.path.join(path, file)
            #print "rename", srcFile, destFile
            shutil.copy(srcFile, destFile)
    return ok

cmake_path = os.path.abspath('toolchain/cmake/bin/cmake.exe')

def run_cmake(platform):
    intermediate_path = '_obj-lib-etc'
    root_path = Path(__file__).parent.resolve()
    build_path = Path(intermediate_path) / platform / 'sharedtec'
    build_path.mkdir(parents=True, exist_ok=True)
    with cwd(build_path):
        cmd = [
            cmake_path,
            '-G', 'Visual Studio 15 2017 Win64',
            str(root_path) # source dir
        ]
        logging.info('Run cmake command: %s', str(cmd))
        subprocess.check_call(cmd)

def find_vs():
	possibleVariants = [r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\VC\Auxiliary\Build\vcvars64.bat",
						r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat",
						r"C:\Program Files (x86)\Microsoft Visual Studio\2017\Enterprise\VC\Auxiliary\Build\vcvars64.bat"]
	for target in possibleVariants:
		if os.path.exists(target):
			return target
	return r"vcvars64.bat"

def build_boost():
    for directory in [str("boost_1_64_0"), str("boost_1_65_0"), str("boost_1_65_1"), str("boost_1_66_0")]:
        boost_dir = "boost-cmake/boost/" + directory
        patch_dir = "boost-cmake/patch/" + directory
        if os.path.exists(patch_dir) and os.path.exists(boost_dir):
            mergeTree(patch_dir, boost_dir, True)
        if os.path.exists(boost_dir):
            with cwd(boost_dir):
                if not os.path.exists("bjam.exe") and os.path.exists("bootstrap.bat"):
                    p1 = subprocess.Popen("cmd /C \"C:/Program Files (x86)/Microsoft Visual Studio/2017/Professional/Common7/Tools/VsDevCmd.bat\" & \"c:/sandbox/sharedtec/boost-cmake/boost/boost_1_66_0/bootstrap.bat\"")
                    p1.wait()
                    #p = subprocess.Popen("bootstrap.bat", cwd=r".")
                    #stdout, stderr = p.communicate()
                if os.path.exists("bjam.exe"):
                	jobsCount = '-j' + str(multiprocessing.cpu_count())
                	subprocess.call([r'bjam', r'--stagedir=stage/x64', jobsCount, r'toolset=msvc', r'address-model=64', r'variant=release',  r'threading=multi', r'link=static', r'runtime-link=static,shared', r'define=_SECURE_SCL=0', r'define=_HAS_ITERATOR_DEBUGGING=0',  r'define=BOOST_TEST_NO_MAIN'])
                	subprocess.call([r'bjam', r'--stagedir=stage/x64', jobsCount, r'toolset=msvc', r'address-model=64', r'variant=debug'  ,  r'threading=multi', r'link=static', r'runtime-link=static,shared', r'define=BOOST_TEST_NO_MAIN'])
                else:
                	print("bjam not found")
                #shutil.rmtree("bin.v2")

def setup():
    if os.path.exists(".git"):
        with cwd('.'):
            subprocess.call(['git', 'submodule', 'update', '--init', '--recursive'])
    elif os.path.exists(".hg"):
        if os.path.exists(".hg") and not os.path.exists("boost-cmake/.git"):            
            subprocess.call([r'git', r'clone', 'https://github.com/nvoronetskiy/boost-cmake.git'])

    run_cmake("windows")
    build_boost()

    # with cwd("Stable"):
    #     msbuild.build('libs.sln', 'Debug', 'x64')


if __name__ == '__main__':
	setup()    
