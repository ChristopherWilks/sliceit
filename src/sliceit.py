#!/usr/bin/env python2.7
#client to access genomic regions via web services that export them by both byte range and genomic coordinate range

import sys
import re
import os
import subprocess
import time
import datetime
import logging
from logging import handlers
import urllib2
import urllib
import base64
import argparse

####CHANGES I'M GOING TO REVERT


#credit for the logging and argparse code goes to Hannes Schmidt
#https://bitbucket.org/cghub/cghub-capture-kit-info/src/9129b8e749210d4b74a428448e01a6217f94e0ee/manage.py?at=master
log = logging.getLogger( os.path.basename( __file__ ) if __name__ == '__main__' else __name__ )

samtools_ = 'samtools'

def slice_resource_by_byte_ranges(url, url_index, samtools, ranges):
    return True

def main( ):
    logging.basicConfig( )
    dir_path = os.getcwd( )
    levels = [ logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG ]

    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter )
    parser.add_argument( '--verbosity',
                         help='Set the level of detail for the console output',
                         default=logging.getLevelName( logging.INFO ),
                         choices=[ logging.getLevelName( l ) for l in levels ] )
    parser.add_argument('-u',help='url of the resource to slice against (usually a BAM file hosted by a web service)',required=True,dest="url") 
    parser.add_argument('-b',help='[default=argment to -u suffixed with .bai] url to the index file (e.g. BAI)',dest="url_index",default=None) 
    parser.add_argument('-s',help='path to samtools binary',dest="samtools",default=samtools_) 
    options = parser.parse_args( )

    url = options.url
    samtools = options.samtools
    url_index = options.url_index

    logging.root.setLevel( logging.getLevelName( options.verbosity ) )
    if not url_index:
        url_index = "%s.bai" % (url) 
    sys.stderr.write("url: %s; index url: %s; samtools path: %s; \n" % (url,url_index,samtools))
    ranges = ["21:9411867-9411867","21:9411867-9483324"]

    byte_ranges = translate_coordinates2bytes(samtools, ranges) 
    slice_resource_by_byte_ranges(url, url_index, samtools, byte_ranges)

if __name__ == '__main__':
    main()
