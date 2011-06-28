#!/usr/bin/python

import time, getopt, sys, ws300interface

# uncomment this to use mysql-db
import MySQLdb as mdb
conn = mdb.connect('localhost', 'ws300', 'Asbxhb24EQsvWLpV', 'ws300')
use_mysql = True
    
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

def save_data_in_mysql(ws300, conn):
  string = "INSERT INTO ws300 SET time=NOW()"
  for i in range(0, 10):
    string += ", s%d_status=%s" % (i, ws300.getSensorStatusValue(i))
    if ws300.isSensorWorking(i):
      string += ", s%d_temp=%s" % (i, ws300.getTemperature(i))
      string += ", s%d_humi=%s" % (i, ws300.getHumidity(i))
  if ws300.isSensorWorking(9):
      string += ", pressure=%s" % ws300.getPressure()
      string += ", rain_abs=%f" % ws300.getRainAmount()
      string += ", wind=%d" % ws300.getWindspeed()

  cursor = conn.cursor();
  cursor.execute("SELECT rain_abs FROM ws300 WHERE rain_abs IS NOT NULL ORDER BY time DESC LIMIT 1")
  old_rain = cursor.fetchone()

  if old_rain:
    diff = ws300.getRainAmount() - float(old_rain[0])
    if diff >= 0:
      string += ", rain_rel=%.5f" % diff
  
  cursor.execute(string)
  conn.commit()

try:
  opts, args = getopt.getopt(sys.argv[1:], "ahf", ["help", "force"])
except getopt.GetoptError, err:
  print "Unexcepted error during getopt"
  sys.exit(2)

conf = {}
conf["printAllSensors"]=0
conf["forceQuery"] = not use_mysql

for o, a in opts:
  if o == "-a":
    conf["printAllSensors"]=1
  elif o in ("-f", "--force"):
    conf["forceQuery"]=True
  elif o in ("-h", "--help"):
    print "Parameter:"
    print "  -a  Alle Sensoren werden in der Ausgabe angezeigt."
    print "  -h  Zeigt diese Hilfe an."
    sys.exit()


ws300 = ws300interface.ws300()
ws300.sensorOfflineAfter = 60

if use_mysql:
    save_data_in_mysql(ws300, conn)

for i in range(0, 10):
  output('sensor_%d_temp' % i, ws300.getTemperature(i))
  output('sensor_%d_humi' % i, ws300.getHumidity(i))
  output('sensor_%d_status' % i, ws300.getSensorStatusValue(i))
output('pressure', ws300.getPressure())
output('windchill', ws300.getWindchillTemperature())
output('rain', int(ws300.getRainAmount()))
output('rain_gauge', ws300.getRainAmount())
output('wind', ws300.getWindspeed())

#output('setHeight', ws300.getSetHeight())
#output('setWaterAmount', ws300.getSetWaterAmount())
#output('setInterval', ws300.getInterval())
sys.exit

# T1 T1 F1 T2 T2 F2 T3 T3 F3 T4 T4 F4 T5 T5 F5 T6 T6 F6 T7 T7 F7 T8 T8 T8 T9 T9 F9 RA-IN WI-ND T0 T0 F0 P-abs *1
#  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36
