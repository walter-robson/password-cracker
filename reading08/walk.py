#!/usr/bin/env python3

import os
import sys

try:
    directory = sys.argv[1]
except IndexError:
    directory = '.'

# TODO: Walk specified directory in sorted order and print out each entry's
# file name

with os.scandir(directory) as entries:
    sentries = sorted(entries, key=lambda a: a.name)
    for entry in sentries:
        print(entry.name)
