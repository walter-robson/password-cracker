#!/usr/bin/env python3

import sys

print(' '.join(
    filter(lambda a: int(a)%2==0, map(lambda a: a.strip(), sys.stdin))
))
