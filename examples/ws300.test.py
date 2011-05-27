#!/usr/bin/python

import time, getopt, sys, ws300interface
    
def output(sensorname, value):
  global conf
  if value!='UNKNOWN' or conf["printAllSensors"]==1:
    sys.stdout.write('%s:%s ' % (sensorname, value))

def echoValues(values):
  for n in range(0, len(values)-1):
    print '%2d' % n,
  print
  for n in range(0, len(values)-1):
    print '%2s' % (hex(ord(values[n]))[2:]),

try:
  opts, args = getopt.getopt(sys.argv[1:], "ah", ["help"])
except getopt.GetoptError, err:
  print "Unexcepted error during getopt"
  sys.exit(2)

conf = {}
conf["printAllSensors"]=0

for o, a in opts:
  if o == "-a":
    conf["printAllSensors"]=1
  elif o in ("-h", "--help"):
    print "Parameter:"
    print "  -a  Alle Sensoren werden in der Ausgabe angezeigt."
    print "  -h  Zeigt diese Hilfe an."
    sys.exit()

ws300 = ws300interface.ws300()
ws300.sensorOfflineAfter = 60

output('last_byte_binary', ws300.convertToBinary(ws300.getUnknownByte()))
output('last_byte_ord', ws300.getUnknownByte())

#output('setHeight', ws300.getSetHeight())
#output('setWaterAmount', ws300.getSetWaterAmount())
#output('setInterval', ws300.getInterval())
sys.exit

# T1 T1 F1 T2 T2 F2 T3 T3 F3 T4 T4 F4 T5 T5 F5 T6 T6 F6 T7 T7 F7 T8 T8 T8 T9 T9 F9 RA-IN WI-ND T0 T0 F0 P-abs *1
#  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36
