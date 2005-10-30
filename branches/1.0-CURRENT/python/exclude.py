#---------------------------------------------------------------
# Project         : Mandrake Linux
# Module          : python
# File            : exclude.py
# Version         : $Id$
# Author          : Frederic Lepied
# Created On      : Mon Feb 11 13:51:02 2002
# Purpose         : simple excluder for python packaging need.
#  usage: python exlcude.py <root dir> <exclude file> <file list>
#
# do not support directory in file list.
#---------------------------------------------------------------

import glob
import sys
import fnmatch

root = sys.argv[1]
root_len = len(root)
exclude_file = sys.argv[2]
full_file = sys.argv[3]

full = open(full_file, 'r').readlines()
exclude = open(exclude_file, 'r').readlines()

exclude_list = []
refinement = []
really_full = []

for l in exclude:
    if l[-1] == '\n':
        l = l[:-1]
    for f in glob.glob(root+l):
        exclude_list.append(f[root_len:])

for l in full:
    if l[-1] == '\n':
        l = l[:-1]
    list = []
    found = 0
    for f in exclude_list:
        if fnmatch.fnmatch(f, l):
            if not found:
                for x in glob.glob(root + l):
                    list.append(x[root_len:])
                found = 1
            try:
                list.remove(f)
            except ValueError:
                pass
            if list == []:
                break
    if found:
        if list != []:
            refinement.extend(list)
    else:
        really_full.append(l)

for f in really_full:
    print f

for f in refinement:
    print f

# exclude.py ends here
