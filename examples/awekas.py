#!/usr/bin/python

import ws300interface, sys
from time import *

ws300 = ws300interface.ws300()

lines = []

if ws300.getSensorStatusValue(9)<16 or ws300.getSensorStatusValue(9)>18:
    sys.exit(1)

lines.append("\n")
lines.append("%s\n" % ws300.getTemperature(9))
lines.append("%s\n" % ws300.getHumidity(9))
lines.append("%s\n" % ws300.getPressure())
lines.append(" \n")
lines.append("%s\n" % ws300.getWindspeed())
lines.append(" \n")
lines.append("%s\n" % strftime("%H:%M", localtime()))
lines.append("%s\n" % strftime("%d.%m.%Y", localtime()))
lines.append(" \n")
lines.append(" \n")

fp = open("/var/www/wetter/awekas.txt","w")
fp.writelines(lines)
fp.close()
