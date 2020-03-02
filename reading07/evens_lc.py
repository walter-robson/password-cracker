#!/usr/bin/env python3

import sys

print(' '.join(
    [a for a in [b.strip() for b in sys.stdin ] if int(a) %2 == 0]
))
