#!/usr/bin/env python3

import sys

def evens(stream):
    for v in stream:
        v = v.strip()
        if int(v) % 2 == 0:
            yield v

print(' '.join(evens(sys.stdin)))
