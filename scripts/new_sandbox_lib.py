#!/usr/bin/env python3

import template, sys, os

def deploy_project(templateName, sourceProjectName, projectName):
	print('deploy:', sourceProjectName, 'as', projectName)
	template.unpack_project(templateName + ".zip", "SandBox", sourceProjectName, projectName)

if __name__ == '__main__':
	if len(sys.argv) == 2:
		deploy_project('_static_library', 'staticLibrary', sys.argv[1])