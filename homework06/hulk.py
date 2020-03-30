#!/usr/bin/env python3

import concurrent.futures
import hashlib
import os
import string
import sys

# Constants

ALPHABET = string.ascii_lowercase + string.digits

# Functions

def usage(exit_code=0):
    progname = os.path.basename(sys.argv[0])
    print(f'''Usage: {progname} [-a ALPHABET -c CORES -l LENGTH -p PATH -s HASHES]
    -a ALPHABET Alphabet to use in permutations
    -c CORES    CPU Cores to use
    -l LENGTH   Length of permutations
    -p PREFIX   Prefix for all permutations
    -s HASHES   Path of hashes file''')
    sys.exit(exit_code)

def md5sum(s):
    ''' Compute md5 digest for given string. '''
    # TODO: Use the hashlib library to produce the md5 hex digest of the given
    # string.
    md = hashlib.md5()
    md.update(s.encode())
    return md.hexdigest()

def permutations(length, alphabet=ALPHABET):
    ''' Recursively yield all permutations of the given length using the
    provided alphabet. '''
    # TODO: Use yield to create a generator function that recursively produces
    # all the permutations of the given length using the provided alphabet.
    for l in alphabet:
        if length == 1:
            yield l
        else:
            for m in permutations(length - 1, alphabet):
                yield l + str(m)


def flatten(sequence):
    ''' Flatten sequence of iterators. '''
    # TODO: Iterate through sequence and yield from each iterator in sequence.
    for x in sequence:
        for y in x:
            yield y

def crack(hashes, length, alphabet=ALPHABET, prefix=''):
    ''' Return all password permutations of specified length that are in hashes
    by sequentially trying all permutations. '''
    # TODO: Return list comprehension that iterates over a sequence of
    # candidate permutations and checks if the md5sum of each candidate is in
    # hashes.
    return [prefix + perm for perm in permutations(length, alphabet) if md5sum(prefix + perm) in hashes ]

def cracker(arguments):
    ''' Call the crack function with the specified arguments '''
    return crack(*arguments)

def smash(hashes, length, alphabet=ALPHABET, prefix='', cores=1):
    ''' Return all password permutations of specified length that are in hashes
    by concurrently subsets of permutations concurrently.
    '''
    # TODO: Create generator expression with arguments to pass to cracker and
    # then use ProcessPoolExecutor to apply cracker to all items in expression.
    arguments = ((hashes, length-1, alphabet, prefix + str(l)) for l in alphabet)
    with concurrent.futures.ProcessPoolExecutor(int(cores)) as executor:
        ly = flatten(executor.map(cracker, arguments))

    return ly

def main():
    arguments   = sys.argv[1:]
    alphabet    = ALPHABET
    cores       = 1
    hashes_path = 'hashes.txt'
    length      = 1
    prefix      = ''
    flags = ['-a', '-c', '-l', '-p', '-s']
    # TODO: Parse command line arguments
    for x in range(len(arguments)):
        if arguments[x-1] in flags:
            continue
        else:
            if arguments[x] == '-h':
                usage(0)
            elif arguments[x] == '-a':
                alphabet = arguments[x+1]
            elif arguments[x] == '-c':
                cores = arguments[x+1]
            elif arguments[x] == '-l':
                length = int(arguments[x+1])
            elif arguments[x] == '-p':
                prefix = arguments[x+1]
            elif arguments[x] == '-s':
                hashes_path = arguments[x+1]
    # TODO: Load hashes set
    hashes = set(map(lambda a: a.rstrip(), open(hashes_path)))
    # TODO: Execute crack or smash function
    if cores == 1 or length ==1:
        outcome = crack(hashes, length, alphabet, prefix)
    else:
        outcome = smash(hashes, length, alphabet, prefix, cores)
    # TODO: Print all found passwords
    for out in outcome:
        print(out)
# Main Execution

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
