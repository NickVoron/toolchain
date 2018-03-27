import os
import configure.utils


# return list of directories witch is Module(contains dir 'Source')


def contain_source(dir_path):

    # print('check {0}'.format(dir_path))
    dir_list = os.listdir(dir_path)

    with configure.utils.cwd(dir_path):
        for dir_name in dir_list:
            # sprint('   internal: {0}'.format(dir_name))
            if os.path.isdir(dir_name) and dir_name == 'Sources':
                return True

    return False


def get_modules():
    dir_list = os.listdir('./')

    for dir_name in dir_list:
        if os.path.isdir(dir_name) and contain_source(dir_name):
            print(dir_name)

    pass


get_modules()
