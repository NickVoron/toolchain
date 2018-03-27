#!/usr/bin/env python3

import template, sys, os

def pack_solution(solutionName):
	print('pack:', solutionName)
	template.pack_solution(solutionName)

if __name__ == '__main__':
	if len(sys.argv) == 2:
		pack_solution(sys.argv[1])