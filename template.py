#!/usr/bin/env python -u

import os
import sys
import argparse

pjoin = os.path.join

DEBUG=False

def debug(msg, *args):
    if DEBUG:
        if args:
            print msg % args
        else:
            print msg
            
def terminate(msg, existatus=1):
    sys.stderr.write(msg+"\n")
    sys.exit(exitstatus)

class Application(object):
    def parse_args(self):
        global DEBUG
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("-d", "--debug", action="store_true", help="Enable debug")
        
        
        args = parser.parse_args()    
        if args.debug:
            DEBUG = True
            
        return args

    def run(self):
        self.parse_args()
        
        return 0




if __name__ == "__main__":
    app = Application()
    sys.exit(app.run())
    