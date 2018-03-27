#!/usr/bin/env python3

import template, sys, os


def deploy(solutionName):
    print('deploy:', solutionName)
    template.unpack_solution("_static_library.zip", "SandBox", solutionName)
    slnfile = "SandBox\\" + solutionName + ".sln"
    os.system("start " + slnfile)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        deploy(sys.argv[1])
    elif len(sys.argv) == 1:
        deploy('HelloLib')
