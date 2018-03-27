import urllib.request
import json
import shutil
import sys
import getopt
import utils
import boost_utils

cmake_proto_path = 'toolchain/scripts/configure/CMakeLists.proto'
cmake_destination_path = 'boost-cmake/CMakeLists.txt'


def fix_cmake(version, boost_beta, beta_version):
    # remove_intermediate()
    # remove_boost()

    parts = version.split('.')
    dash_version = '_'.join(parts)

    if boost_beta:
        release_type = 'beta'
        version += '.beta.{0}'.format(beta_version)
        dash_version += '_b{0}'.format(beta_version)
    else:
        release_type = 'release'

    json_url = 'https://dl.bintray.com/boostorg/{0}/{1}/source/boost_{2}.7z.json'.format(release_type, version, dash_version)
    print(json_url)
    response = urllib.request.urlopen(json_url)

    js_response = response.read()
    str_response = js_response.decode("utf-8")

    str_lenght = len(str_response)
    if str_response[str_lenght-3:str_lenght-2] == ',':
        str_response = str_response[:str_lenght-3] + str_response[str_lenght-2:]
        # print(str_response)

    j_data = json.loads(str_response)

    file = j_data['file']
    sha256 = j_data['sha256']

    print(file)
    print(sha256)

    shutil.copy2(cmake_proto_path, cmake_destination_path)
    utils.replce_cmakefile(cmake_destination_path, '_dot_path_part_', version)
    utils.replce_cmakefile(cmake_destination_path, '_file_path_part_', file)
    utils.replce_cmakefile(cmake_destination_path, '_sha256_', sha256)
    utils.replce_cmakefile(cmake_destination_path, '_release_type_path_', release_type)

    pass


def run():
    input_args = sys.argv[1:]   # skip first param - path to python file
    optlist, args = getopt.getopt(input_args, '', ['version=', 'beta='])

    boost_update_version = ''
    boost_beta = False
    beta_version = 1
    for opt_type, value in optlist:
        if opt_type == '--version':
            boost_update_version = value
            pass
        if opt_type == "--beta":
            boost_beta = True
            beta_version = value
            pass
        pass

    if not boost_beta:
        print("update boost on version: {0}".format(boost_update_version))
    else:
        print("update boost on version: {0}, beta:{1}".format(boost_update_version, boost_beta))
        pass

    boost_utils.remove_intermediate()
    boost_utils.remove_boost()
    boost_utils.get_boost()

    fix_cmake(boost_update_version, boost_beta, beta_version)

    boost_utils.run_boost_cmake()
    boost_utils.boost_build()

    pass


if __name__ == '__main__':
    run()
