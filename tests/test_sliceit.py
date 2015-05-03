#!/usr/bin/env python2.7

import sys
import sys
import os
import unittest
import subprocess
import urllib2
import urllib

#where_am_i = os.path.basename( __file__ ) if __name__ == '__main__' else __name__
TEST_PATH = os.path.dirname(os.path.realpath(os.path.abspath(__file__)))
SCRIPT_PATH = "%s/../src/" % TEST_PATH
sys.path.append(os.path.dirname(TEST_PATH))
sys.path.append(os.path.dirname(SCRIPT_PATH))

sys.stderr.write("sys path %s" % sys.path)
import sliceit

SAMTOOLS = 'samtools'
TEST_URL = "file://%s/data/a2e377ac-602c-4bc2-a992-c69001149308.bam" % (SCRIPT_PATH)
TEST_SLICER_URL = 'http://127.0.0.1:1443/analyses/a2e377ac-602c-4bc2-a992-c69001149308/a2e377ac-602c-4bc2-a992-c69001149308.bam'


class TestSliceIt(unittest.TestCase):

    def test_slice_resource_by_byte_range(self):
        passed = sliceit.slice_resource_by_byte_range(TEST_URL, "%s.bai" % TEST_URL, SAMTOOLS, [])
        self.assertEqual(passed,True)
        
if __name__ == '__main__':
    unittest.main()
