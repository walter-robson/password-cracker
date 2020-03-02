#!/usr/bin/env python3

import collections
import os
import sys

import requests

# Constants

URL     = 'https://yld.me/raw/axPa'
TAB     = ' '*8
GENDERS = ('M', 'F')
ETHNICS = ('B', 'C', 'N', 'O', 'S', 'T', 'U')

# Functions

def usage(status=0):
    ''' Display usage information and exit with specified status '''
    progname = os.path.basename(sys.argv[0])
    print(f'''Usage: {progname} [options] [URL]

    -y  YEARS   Which years to display (default: all)
    -p          Display data as percentages.
    -G          Do not include gender information.
    -E          Do not include ethnic information.
    ''')
    sys.exit(status)

def load_demo_data(url=URL):
    ''' Load demographics from specified URL into dictionary

    >>> load_demo_data('https://yld.me/raw/ilG').keys()
    dict_keys(['2013', '2014', '2015', '2016', '2017', '2018', '2019'])

    >>> load_demo_data('https://yld.me/raw/ilG')['2013'] == \
            {'M': 1, 'B': 2, 'F': 1, 'TOTAL': 2}
    True

    >>> load_demo_data('https://yld.me/raw/ilG')['2019'] == \
            {'M': 1, 'U': 2, 'F': 1, 'TOTAL': 2}
    True
    '''
    # TODO: Request data from url and load it into dictionary organized in the
    # following fashion:
    #
    #   {'year': {'gender': count, 'ethnic': count, 'TOTAL': count}}
    data = {}

    raw = requests.get(url)
    raw = raw.text
    raw = raw.split('\n')

    for line in raw:
        if line is raw[0] or line == '':
            continue
        line = line.split(',')
        data[line[0]] = data.get(line[0],{})
        data[line[0]][line[1]] = data[line[0]].get(line[1],0) + 1
        data[line[0]][line[2]] = data[line[0]].get(line[2],0) + 1

    #store number of students for each year in a dict
    for entry in data:
        data[entry]['TOTAL'] = data[entry].get('TOTAL',0) + data[entry]['M'] + data[entry]['F']

    return data

def print_demo_separator(years, char='='):
    ''' Print demographics separator

    Note: The row consists of the 8 chars for each item in years + 1.

    >>> print_demo_separator(['2012', '2013'])
    ========================
    '''
    # TODO: Print row of separator characters
    num = (len(years)) + 1
    print(f'{char}'*num*8)

def print_demo_years(years):
    ''' Print demographics years row

    Note: The row is prefixed by 4 spaces and each year is right aligned to 8
    spaces ({:>8}).

    >>> print_demo_years(['2012', '2013'])
            2012    2013
    '''
    # TODO: Print row of years
    row = '    '
    for year in sorted(years):
        row = row + f'{year:>8}'
    print(row)

def print_demo_fields(data, years, fields, percent=False):
    ''' Print demographics information (for particular fields)

    Note: The first column should be a 4-spaced field name ({:>4}), followed by
    8-spaced right aligned data columns ({:>8}).  If `percent` is True, then
    display a percentage ({:>7.1f}%) rather than the raw count.

    >>> data  = load_demo_data('https://yld.me/raw/ilG')
    >>> years = sorted(data.keys())
    >>> print_demo_fields(data, years, GENDERS, False)
       M       1       1       1       1       1       1       1
       F       1       1       1       1       1       1       1
    '''
    # TODO: For each field, print out a row consisting of data from each year.
    if(fields is GENDERS):
        fields = sorted(fields, reverse = True)
    years = sorted(years)

    for c in fields:
        row = ' '*3 + c
        for y in years:
            if percent:
                val = data[y].get(c,0) / data[y]['TOTAL'] * 100
                row = row + f'{val:>7.1f}%'
            else:
                row = row + f'{data[y].get(c,0):>8}'
        print(row)

def print_demo_data(data, years=None, percent=False, gender=True, ethnic=True):
    ''' Print demographics data for the specified years and attributes '''
    # TODO: Verify the years parameter (if None then extract from data,
    # otherwise use what is given).  Ensure years is sorted.
    # TODO: Print years header with separator
    print_demo_years(years)
    print_demo_separator(years)

    # TODO: Print gender and ethic data if enabled
    if gender:
        print_demo_gender(data, years, percent)
    if ethnic:
        print_demo_ethnic(data, years, percent)


def print_demo_gender(data, years, percent=False):
    ''' Print demographics gender information '''
    print_demo_fields(data, years, GENDERS, percent)
    print_demo_separator(years, '-')

def print_demo_ethnic(data, years, percent=False):
    ''' Print demographics ethnic information '''
    print_demo_fields(data, years, ETHNICS, percent)
    print_demo_separator(years, '-')

def main():
    ''' Parse command line arguments, load data from url, and then print
    demographic data. '''
    # TODO: Parse command line arguments
    arguments = sys.argv[1:]
    url       = URL
    years     = None
    gender    = True
    ethnic    = True
    percent   = False

    # TODO: Load data from url and then print demograpic data with specified
    # arguments
    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        usage()
    for x in range(len(sys.argv[1:])):
        if arguments[x-1] == '-y':
            continue
        elif arguments[x] == '-y':
            years = arguments[x+1]
            years = years.split(',')
        elif arguments[x] == '-p':
            percent = True
        elif arguments[x] == '-G':
            gender = False
        elif arguments[x] == '-E':
            ethnic = False
        elif arguments[x][:4] == 'http':
            url = arguments[x]
        else:
            usage(1)

    data = load_demo_data(url)
    if not years:
        years = data.keys()
    print_demo_data(data, years, percent, gender, ethnic)


# Main Execution

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
