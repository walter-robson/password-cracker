#!/usr/bin/env python3

import os
import signal
import sys
import time

# Functions

def usage(status=0):
    ''' Display usage message for program and exit with specified status. '''
    progname = os.path.basename(sys.argv[0])
    print(f'''Usage: {progname} [options] command...
Options:
    -t SECONDS  Timeout duration before killing command (default is 10)
''')
    sys.exit(status)

def error(message, status=1):
    ''' Display error message and exit with specified status. '''
    print(message, file=sys.stderr)
    sys.exit(status)

def alarm_handler(signum, frame):
    ''' Alarm handler that raises InterruptedError '''
    raise InterruptedError

def timeit(argv, timeout=10):
    ''' Run command specified by argv for at most timeout seconds.

    - After forking, the child executes the specified command.

    - After forking, the parent does the following:
        - Registers a handler for SIGALRM
        - Set alarm for specified timeout
        - Waits for child process
        - If wait is interrupted, kills the child process and wait again
        - Prints total elapsed time
        - Exits with the status of the child process
    '''
    try:
        rc = os.fork()
    except OSError:
        sys.exit(1)

    if rc == 0: #child
        try:
            os.execvp(argv[0], argv)
        except OSError:
            sys.exit(1)
    else:  #parent
        starttime = time.time()
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(timeout)
        try:
            rc, status = os.wait()
        except InterruptedError:
            try:
                os.kill(rc, signal.SIGKILL)
            except OSError:
                sys.exit(1)

        print(f'Time Elapsed: {time.time()-starttime:.2f}')

        try:
            if os.WIFEXITED(status):
                sys.exit(os.WEXITSTATUS(status))
        except UnboundLocalError:
            sys.exit(os.WTERMSIG(signal.SIGKILL))

def main():
    ''' Parse command line options and then execute timeit with specified
    command and timeout. '''
    time = 10
    command = []
    arguments = sys.argv[1:]
    if not arguments:
        usage(1)
    for i in range(len(arguments)):
        if arguments[i] == '-h':
            usage(0)
        if arguments[i] == '-t':
            time = int(arguments[i+1])
        elif arguments[i-1] != '-t':
            command.append(arguments[i])
    if not command:
        usage(1)

    timeit(command, time)




# Main Execution

if __name__ == '__main__':
    main()
