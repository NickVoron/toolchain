#!/usr/bin/env python3

import template, sys, os


def deploy_project(templateName, sourceProjectName, projectName):
    print('deploy:', sourceProjectName, 'as', projectName)
    template.unpack_project(templateName + ".zip", "SandBox", sourceProjectName, projectName)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        deploy_project('_standalone_tests', sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 1:
        deploy_project('_standalone_tests', 'ConsoleTest', 'HelloWorld')
