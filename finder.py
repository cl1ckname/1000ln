import sys
import argparse
import threading
import re
import os
import time
from random import randint

MATCH = r'^.*[\\\/](.*)$'  # regex to validate optional path
paths = []


def threadingSearch(name, path, threads):
    '''recursive function to search for a given file for a given path 


    Keyword arguments:
    name -- the name of file
    path -- the start directory


    '''
    try:
        for element in os.scandir(path):
            if element.is_file():
                if element.name == name:
                    paths.append(element.path)
            else:
                while threading.active_count() > int(threads):
                    time.sleep(0.5)
                thread = threading.Thread(target=threadingSearch, args=(
                    name, element.path, threads), daemon=True)
                thread.start()

    except PermissionError:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start', default='C:\\')
    parser.add_argument('-t', '--threads', default='500')
    args = parser.parse_args(sys.argv[2:])
    if re.match(MATCH, args.start):
        t = threading.Thread(target=threadingSearch, args=(
            sys.argv[1], args.start, args.threads))
        t.start()
        while threading.active_count() > 1:
            time.sleep(2)
        if len(paths):
            print('Results:', *paths, sep='\n')
        else:
            print('Did not match')
    else:
        print('Unvalid path')
