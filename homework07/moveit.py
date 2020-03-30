#!/usr/bin/env python3

import atexit
import os
import sys
import tempfile

# Functions

def usage(status=0):
    ''' Display usage message for program and exit with specified status. '''
    print(f'Usage: {os.path.basename(sys.argv[0])} files...')
    sys.exit(status)

def save_files(files):
    ''' Save list of files to a temporary file and return the name of the
    temporary file. '''
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        for file in files:
            tf.write(bytes(file.encode()))
            tf.write(b'\n')
        return tf.name

def edit_files(path):
    ''' Fork a child process to edit the file specified by path using the user's
    default EDITOR (use "vim" if not set).  Parent waits for child process and
    returns whether or not the child was successful. '''
    try:
        rc = os.fork()
    except OSError:
        sys.exit(1)
    if rc == 0: #child
        os.execlp(os.environ.get('EDITOR', 'vim'), os.environ.get('EDITOR', 'vim'), path)
    else:  #parent
        rc, status = os.wait()
    if os.WEXITSTATUS(status):
        return False
    else:
        return True

def move_files(files, path):
    ''' For each file in files and the corresponding information from the file
    specified by path, rename the original source file to the new target path
    (if the names are different).  Return whether or not all files were
    successfully renamed. '''
    for tuples in zip(files, open(path).readlines()):
        if not tuples[0] == tuples[1].rstrip():
            try:
                os.rename(tuples[0], tuples[1].rstrip())
            except OSError:
                return False
    return True


def main():
    ''' Parse command line arguments, save arguments to temporary file, allow
    the user to edit the temporary file, move the files, and remove the
    temporary file. '''
    # TODO: Parse command line arguments
    arguments = sys.argv[1:]
    if not arguments:
        usage(1)
    for i in arguments:
        if i == '-h':
            usage(1)

    # TODO: Save files (arguments)
    filename = save_files(arguments)

    # TODO: Register unlink to cleanup temporary file
    atexit.register(os.unlink, filename)

    # TODO: Edit files stored in temporary file
    bool1 = edit_files(filename)

    # TODO: Move files stored in temporary file
    bool2 = move_files(arguments, filename)

    if not bool1:
        sys.exit(1)
    if not bool2:
        sys.exit(1)
# Main Execution

if __name__ == '__main__':
    main()
