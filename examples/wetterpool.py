#!/usr/bin/python

import ws300interface, sys
from time import *

ws300 = ws300interface.ws300()

if ws300.getSensorStatusValue(9)<16 or ws300.getSensorStatusValue(9)>18:
    sys.exit(1)
       
lines = []

lines.append("(TCUR_ %s)\n" % ws300.getTemperature(9))
lines.append("(TMIN_ - -)\n")
lines.append("(TMAX_ - -)\n")
lines.append("(TCH1_ - -)\n")
lines.append("(TDM1_ - -)\n")
lines.append("(T5MIN - -)\n")
lines.append("(TCM30 - -)\n")
lines.append("(RHCUR %s)\n" % ws300.getHumidity(9))
lines.append("(RRH1_ - -)\n")
lines.append("(RRH2_ - -)\n")
lines.append("(RRH6_ - -)\n")
lines.append("(RRH12 - -)\n")
lines.append("(RRH24 - -)\n")
lines.append("(RRD1_ - -)\n")
lines.append("(RRM1_ - -)\n")
lines.append("(RRY1_ - -)\n")
lines.append("(RRDM1 - -)\n")
lines.append("(SUND1 - -)\n")
lines.append("(SUNH1 - -)\n")
lines.append("(WCUR_ %s)\n" % ws300.getWindspeed())
lines.append("(WDIR_ - -)\n")
lines.append("(WCURA - -)\n")
lines.append("(WDIRA - -)\n")
lines.append("(WMX__ - -)\n")
lines.append("(PCUR_ %s)\n" % ws300.getPressure())
lines.append("(PCH1_ - -)\n")
lines.append("(PCH3_ - -)\n")
lines.append("(CLCNB - -)\n")
lines.append("(HGTNN 180)\n")
lines.append("(DAONI - -)\n")
lines.append("(SNHGT - -)\n")
lines.append("(SNHTD - -)\n")
lines.append("(SNL__ - -)\n")
lines.append("(LXCUR - -)\n")
lines.append("(LXMAX - -)\n")

lines.append("(RRY1__ - -)\n")
lines.append("(WCURA_ - -)\n")
lines.append("(WDIRA_ - -)\n")

lines.append("(TIME_ %s)\n" % strftime("%H:%M", localtime()))
lines.append("(DATE_ %s)\n" % strftime("%d.%m.%Y", localtime()))
lines.append("(PLGNV 1.2)\n")

fp = open("/var/www/wetter/wetterpool.txt","w")
fp.writelines(lines)
fp.close()
