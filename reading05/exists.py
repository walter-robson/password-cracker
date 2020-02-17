#!/usr/bin/env python3

import os
import sys

def exir_func(file= ' '):
	sys.exit(f'{file} does not exists!')

for arg in sys.argv:
	if os.path.exists('./' + arg):
		print(f'{arg} exists!')
	else: 
		exit_func(arg);
