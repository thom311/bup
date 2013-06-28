#!/usr/bin/env python
import sys, os, errno, stat
import timeit
from bup import options, git, vfs
from bup.helpers import *
bfuse = __import__('fuse-cmd')


optspec = """
bup walk-vfs [nrepeat] [paths ...]
--
"""
o = options.Options(optspec)
(opt, flags, extra) = o.parse(sys.argv[1:])


git.check_repo_or_die()
top = vfs.RefList(None)
f = bfuse.BupFs(top)

def walk(d, depth=0):
    #print("walk[" + str(depth) + "]>> " + d + " <<")
    for entry in f.readdir(d, None):
        name = entry.name
        n = os.path.join(d, name)
        #print("list[" + str(depth) + "]>> " + n)
        if name == '.' or name == '..':
            continue
        attr = f.getattr(n)
        if isinstance( attr, ( int, long ) ):
            print("ERROR getattr(" + n + ") = " + os.strerror(attr));
        if stat.S_ISDIR(attr.st_mode):
            walk(n, depth+1)

def lwalk(d):
    node = top.resolve(d)
    walk(node.fullname())

repeat = 1
if extra:
    repeat = int(extra[0])
    del extra[0]

if not extra:
    extra = [ '/' ]
def execute():
    for d in extra:
        lwalk(d)

s = 0
t0 = None
for i in range(0,repeat):
    t = timeit.timeit(execute, number=1)
    if t0 is None:
        t0 = t
    print("Run #" + str(i) + " took " + repr(t) + " (" + repr(t/t0*100.0) + " %)")
    s += t
if repeat > 1:
    print("Repeated Runs took in average " + repr((s-t0)/(repeat-1)) + " (" + repr(((s-t0)/(repeat-1))/t0*100.0) + " %)")
print("All runs took " + repr(s))
