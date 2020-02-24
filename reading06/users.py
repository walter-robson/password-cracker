#!/usr/bin/env python3

import csv

# Constants

PATH = '/etc/passwd'

# TODO: Loop through ':' delimited data in PATH and extract the fifth field
# (user description)
usrList = []
csvFile = csv.reader(open(PATH, newline = ''), delimiter = ':')

for row in csvFile:
    usrList.append(row[4])

# TODO: Print user descriptions in sorted order
usrList = sorted(usrList)
for usr in usrList:
    if usr:
        print(usr)
