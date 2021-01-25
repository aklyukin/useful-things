#!/usr/bin/python3

import os
import sys
from plumbum import local

if len(sys.argv) > 1:
    startpath = sys.argv[1]
else:
    startpath = os.getcwd()

def cue_check(cuefile):
    with open(cuefile) as cf:
        tracks_count = 0
        flac_file = ''
        for line in cf:
            if line.startswith('FILE '):
                if flac_file == '':
                    flac_file = line.split('"')[1]
                else:
                    return None
            elif line.startswith('  TRACK '):
                tracks_count += 1
    if tracks_count > 1:
        return flac_file
    else:
        return None

for root, dirs, files in os.walk(startpath):
    for f in files:
        if ((os.extsep in f) and (f.split(os.extsep)[-1] == 'cue')):
            print('===============================================')
            print(root)
            flac_file = cue_check(root + os.sep + f)
            if flac_file:
               with local.cwd(os.path.join(root)):
                    print(os.getcwd())
                    print(flac_file)
                    print(f)
                    print(local.cmd.shnsplit("-f", f, "-t", "%n-%t", "-o", "flac", flac_file))
                    os.remove(flac_file)
