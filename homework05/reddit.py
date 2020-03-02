#!/usr/bin/env python3

import os
import sys

import requests

# Constants

ISGD_URL = 'http://is.gd/create.php'

# Functions

def usage(status=0):
    ''' Display usage information and exit with specified status '''
    print('''Usage: {} [options] URL_OR_SUBREDDIT

    -s          Shorten URLs using (default: False)
    -n LIMIT    Number of articles to display (default: 10)
    -o ORDERBY  Field to sort articles by (default: score)
    -t TITLELEN Truncate title to specified length (default: 60)
    '''.format(os.path.basename(sys.argv[0])))
    sys.exit(status)

def load_reddit_data(url):
    ''' Load reddit data from specified URL into dictionary

    >>> len(load_reddit_data('https://reddit.com/r/nba/.json'))
    27

    >>> load_reddit_data('linux')[0]['data']['subreddit']
    'linux'
    '''
    # TODO: Verify url parameter (if it starts with http, then use it,
    # otherwise assume it is just a subreddit).
    if 'http' not in url:
        url = 'https://www.reddit.com/r/' + url + '/.json'
    elif '.json' not in url:
        url = url + ".json"

    headers  = {'user-agent': 'reddit-{}'.format(os.environ.get('USER', 'cse-20289-sp20'))}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['data']['children']

def shorten_url(url):
    ''' Shorten URL using is.gd service

    >>> shorten_url('https://reddit.com/r/aoe2')
    'https://is.gd/dL5bBZ'

    >>> shorten_url('https://cse.nd.edu')
    'https://is.gd/3gwUc8'
    '''
    # TODO: Make request to is.gd service to generate shortened url.
    newURL = requests.get(ISGD_URL, params={'format': 'json', 'url': url})
    newURL = newURL.json()

    return newURL['shorturl']

def print_reddit_data(data, limit=10, orderby='score', titlelen=60, shorten=False):
    ''' Dump reddit data based on specified attributes '''
    # TODO: Sort articles stored in data list by the orderby key, and then
    # print out each article's index, title, score, and url using the following
    # format:
    #
    #   print(f'{index:4}.\t{title} (Score: {score})\n\t{url}')
    #
    # Note: Trim or modify the output based on the keyword arguments to the function.
    rev = False
    if orderby == 'score':
        rev = True

    ps = data
    ps = sorted(ps, key=lambda f: f['data'][orderby], reverse=rev)

    for index, p in enumerate(ps,1):
        row = ''
        if index > 1:
            print('')
            
        py = p['data']['title'][:int(titlelen)]
        row = row + f"{index:>4}.\t{py}"
        row = row + f" (Score: {p['data']['score']})"
        print(row)

        ly = p['data']['url']
        if shorten:
            ly = shorten_url(ly)
        print(f'\t{ly:>4}')
        if index == int(limit):
            break

def main():
    # TODO: Parse command line arguments
    arguments = sys.argv[1:]
    url       = None
    limit     = 10
    orderby   = 'score'
    titlelen  = 60
    shorten   = False

    # TODO: Load data from url and then print the data
    numArg = int(len(sys.argv))
    if numArg == 1 or sys.argv[1] == '-h':
        usage(0)

    for x in range(len(arguments)-1):
        if arguments[x] == '-s':
            shorten = True
        if arguments[x] == '-n':
            limit = arguments[x+1]
        if arguments[x] == '-o':
            orderby = arguments[x+1]
        if arguments[x] == '-t':
            titlelen = arguments[x+1]
    url = arguments.pop()
    data = load_reddit_data(url)
    print_reddit_data(data, limit, orderby, titlelen, shorten)
# Main Execution

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
