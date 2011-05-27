#!/usr/bin/python

import time, getopt, sys, ws300interface

ws300 = ws300interface.ws300()

for i in range(1, 10):
    status = ws300.getSensorStatusValue(i)
    print 'sensor %d: %d ' % (i, status),
    status = status - 16

    if status==1 or status==2:
        print '!'
    elif status==3 or status==4:
        print '!!'
    elif status>4:
        print '! ! ! !'
    else:
        print ''

