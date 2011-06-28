import serial, time, random, sys
from datetime import datetime, timedelta

# uncomment this to use mysql-db
import MySQLdb as mdb
conn = mdb.connect('localhost', 'ws300', 'Asbxhb24EQsvWLpV', 'ws300')
use_mysql = True

class ws300:
  data = ""
  devData = ""
  isLiveData = True
  # How many messages may be lost before a sensor gets noted as being "offline"
  sensorOfflineAfter = 2
  # force this interface to only use live data
  forceLiveData = False
  # max age in minutes to use old values from the database
  maxOldDataAge = 6
  
  def unescapeRawData(self, data):
    realData = ""
    pos = 0
    while pos<len(data):
      if data[pos] == '\xF8':
        # Next Byte is escaped - we have to decrease it
        realData += chr(ord(data[pos+1])-1)
        pos += 2
      else:
        # Normal Byte
        realData += data[pos]
        pos += 1
    return realData
  
  def processSensorData(self, data):
    realData = self.unescapeRawData(data[2:-1])
    if len(realData)!=37:
      return ""
      #raise Exception('Data length after processing is wrong')
    return realData
  
  def processDevData(self, data):
    realData = self.unescapeRawData(data[2:-1])
    if len(realData)!=14:
      return ""
      #raise Exception('Data length after processing is wrong')
    return realData
    
  def connectAndGetData(self):
    # try to get the latest record from the db
    if use_mysql and not self.forceLiveData:
        cursor = conn.cursor()
        cursor.execute("SELECT time, raw_data, raw_dev_data FROM ws300 ORDER BY time DESC LIMIT 1")
        row = cursor.fetchone()
        if (row and (datetime.now() - row[0]) < timedelta(minutes=self.maxOldDataAge) and row[1] and row[2] and len(row[1])==37 and len(row[2])==14):
            self.data = row[1]
            self.devData = row[2]
            self.isLiveData = False
            return ""
    
    i = 1
    while i<30 and (self.data=="" or self.devData=="") :
      if i>1:
        time.sleep(random.random())
      try:
        ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=0.5, parity=serial.PARITY_EVEN)
        ser.open()
        ser.setRTS(0)
        ser.setDTR(1)
        # Just write some data to "initialize" the port. Shouldn't be necessary, but is...
        ser.write('\xFE\x33\xFC')
        ser.read(100)
        ser.write('\xFE\x33\xFC')
        ser.read(100)

        if self.data=="":
          ser.write('\xFE\x33\xFC')
          result = ser.read(100)
          if result[0:2]=='\xFE\x33' and result[-1]=='\xFC':
            self.data = self.processSensorData(result)
        
        if self.devData=="":
          ser.write('\xFE\x32\xFC')
          result = ser.read(100)
          if result[0:2]=='\xFE\x32' and result[-1]=='\xFC':
            self.devData = self.processDevData(result)
          
        ser.close()
      except OSError:
        pass
      i += 1
      
    if self.data=="" or self.devData=="":
      raise Exception('Couldn\'t get data from WS300.')

  def __init__(self, forceLiveData=False):
    self.forceLiveData = forceLiveData
    self.connectAndGetData()
    if (self.isLiveData and use_mysql):
      self.save_data_to_mysql()

  def save_data_to_mysql(self):
    string = "INSERT INTO ws300 SET time=NOW()"
    for i in range(0, 10):
      string += ", s%d_status=%s" % (i, self.getSensorStatusValue(i))
      if self.isSensorWorking(i):
        string += ", s%d_temp=%s" % (i, self.getTemperature(i))
        string += ", s%d_humi=%s" % (i, self.getHumidity(i))
    if self.isSensorWorking(9):
      string += ", pressure=%s" % self.getPressure()
      string += ", rain_abs=%f" % self.getRainAmount()
      string += ", wind=%d" % self.getWindspeed()
    string += ", raw_data=%s, raw_dev_data=%s"
    cursor = conn.cursor();
    cursor.execute("SELECT rain_abs FROM ws300 WHERE rain_abs IS NOT NULL ORDER BY time DESC LIMIT 1")
    old_rain = cursor.fetchone()
    if old_rain:
      diff = self.getRainAmount() - float(old_rain[0])
      if diff >= 0:
        string += ", rain_rel=%.5f" % diff
    cursor.execute(string, (mdb.Binary(self.data), mdb.Binary(self.devData)))
    conn.commit()

  def getTemperature(self, sensor):
    if sensor>=1 and sensor<=9:
      offset = (sensor-1)*3
    elif sensor==0:
      offset = 31
    else:
      raise Exception('Unknown sensor number')
    if not self.isSensorWorking(sensor):
      return 'UNKNOWN'
    #if self.data[offset]=='\x00' and self.data[offset+1]=='\x00':
    #  return 'UNKNOWN'
    temp = ord(self.data[offset+1])/10.0
    if self.data[offset]=='\xFF':
      temp -= 25.5
    elif self.data[offset]=='\x01':
      temp += 25.5
    return temp
  
  def getHumidity(self, sensor):
    if sensor>=1 and sensor<=9:
      offset = (sensor-1)*3+2
    elif sensor==0:
      offset = 33
    else:
      raise Exception('Unknown sensor number')
    if not self.isSensorWorking(sensor):
      return 'UNKNOWN'
    return ord(self.data[offset])
  
  def getRainAmount(self):
    if not self.isSensorWorking(9):
      return "UNKNOWN"
    mmPerMovement = 0.295
    value = (ord(self.data[27])*255+ord(self.data[28]))*mmPerMovement
    if value==0.0:
      return 0
    return value
  
  def getUnknownByte(self):
    return ord(self.data[36])
    
  def convertToBinary(self, n):
    s=''
    while n:
      s = str(n % 2) + s
      n = n / 2
    return s
    
  def getWindspeed(self):
    if not self.isSensorWorking(9):
      return 'UNKNOWN'
    wind = (ord(self.data[29])*255+ord(self.data[30]))/10.0
    if wind==0.0:
      return 0
    return wind
    
  def getPressure(self):
    if self.data[34]=='\x00' and self.data[35]=='\x00':
      return 'UNKNOWN'
    # Hennen liegt auf ungef. 170m ueber NN - also +20 hPa
    return (ord(self.data[34])*255+ord(self.data[35])+20)
    
  def isSensorWorking(self, sensor):
    if sensor==0:
      return True
    if sensor<0 or sensor >9:
      raise Exception("Unknown Sensor")
    offset = sensor-1
    #print "Sensor", sensor, "hat den Status:", ord(self.devData[offset])
    value = ord(self.devData[offset])
    return (value>=16 and value<=16+self.sensorOfflineAfter)
  
  def getSensorStatusValue(self, sensor):
    if sensor==0:
      return 16
    if sensor<0 or sensor >9:
      raise Exception("Unknown Sensor")
    offset = sensor-1
    value = self.devData[offset]
    return ord(value)
    
  def getSetHeight(self):
    return ord(self.devData[10])*255+ord(self.devData[11])
  
  def getSetWaterAmount(self):
    return (ord(self.devData[12])*255+ord(self.devData[13]))
    
  def getInterval(self):
    return ord(self.devData[10])
    
  def calcWindchillTemperature(self, temp, wind):
    return  13.12 + 0.6215*temp - 11.37*(wind**0.16) + 0.3965*temp*(wind**0.16)
    
  def getWindchillTemperature(self):
    t = self.getTemperature(9)
    if t=="UNKNOWN":
      return "UNKNOWN"
    w = self.getWindspeed()
    if w=="UNKNOWN":
      return "UNKNOWN"
    if w<1.34:
      return t
    return round(self.calcWindchillTemperature(t, w), 2)


  
