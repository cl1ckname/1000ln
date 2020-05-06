import sys
import argparse
import threading

import re
import os
import time


MATCH = r'^.*[\\\/](.*)$' #regex to validate optional path
paths = []

def threadingSearch(name,path):
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
                thread = threading.Thread(target=threadingSearch,args=(name,element.path))
                thread.start()
    except PermissionError:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument ('-s', '--start', default='C:\\')
    args = parser.parse_args(sys.argv[2:])
    if re.match(MATCH,args.start):
        t = threading.Thread(target=threadingSearch,args=(sys.argv[1],args.start))
        t.start()
        t.join()
        while threading.active_count() > 1:
            time.sleep(1)
        if len(paths):
            print(*paths,sep = '\n')
        else:
            print('Did not match')
    else:
        print('Unvalid path')