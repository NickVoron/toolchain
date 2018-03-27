#!/usr/bin/env python3

import template, sys, os

def deploy_project_to_sln(templateName, sourceProjectName, projectName, solutionName):
	print('deploy:', sourceProjectName, 'as', projectName)
	proj = template.unpack_project(templateName + ".zip", "AtomicNet", sourceProjectName, projectName)
	template.add_project_to_solution(os.path.abspath(proj), solutionName)

def deploy_static_lib(projectName, solutionName):
	deploy_project_to_sln('_static_library', 'staticLibrary', projectName, solutionName)

def deploy_console_app(projectName, solutionName):
	deploy_project_to_sln('_standalone_tests', 'ConsoleTest', projectName, solutionName)

def deploy_visual_app(projectName, solutionName):
	deploy_project_to_sln('_standalone_tests', 'VisualTest', projectName, solutionName)

if __name__ == '__main__':
	if len(sys.argv) > 2:
		projectName = sys.argv[2]
		solutionName = sys.argv[1]
		if len(sys.argv) == 3:
			deploy_static_lib(projectName, solutionName)
		elif len(sys.argv) == 4:
			projectType = sys.argv[3]
			if projectType == 'l':
				deploy_static_lib(projectName, solutionName)
			elif projectType == 'c':
				deploy_console_app(projectName, solutionName)
			elif projectType == 'v':
				deploy_visual_app(projectName, solutionName)