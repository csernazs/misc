#!/usr/bin/python

import os
import argparse
from fnmatch import fnmatch

def get_files(path, expr):
    for root, dirs, files in os.walk(path, followlinks=True):
        for file in files:
            if fnmatch(file, expr):
                yield os.path.join(root, file)

def process_files(filelist):
    return {os.path.basename(file): file for file in filelist}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir1", help="Directory to compare")
    parser.add_argument("dir2", help="Directory to compare")
    parser.add_argument("-i", "--include", help="Include files maching to this glob", default="*")

    args = parser.parse_args()
    
    
    files1 = process_files(get_files(args.dir1, args.include))
    files2 = process_files(get_files(args.dir2, args.include))
    
    for file in sorted(set(files1.keys())-set(files2.keys())):
        print files1[file]
    
if __name__ == "__main__":
    main()
    