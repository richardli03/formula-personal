"""
objective - grab data from serial, parse, pass into redis
timeseries database in realtime
"""

import serial
import time
from redis import Redis
from redistimeseries.client import Client
import json

# Data stream parent class with main pass_data() method call
# 2-3 data stream children - serial stream, logfile stream, custom pass_data() methods

class DataStream(object):
    def __init__(self, data_channels):
        # self.start_stream = True
        self.data_channels = data_channels

    # def close_stream(self):
    #     self.start_stream = False

    def return_data_channels(self):
        return self.data_channels


class ArduinoSerialIn(DataStream):
    """
    Class to represent arduino serial datastream object in for testing purposes
    """

    def __init__(
        self, baudrate=9600, port_name="/dev/ttyUSB0", data_channels=["arduino_data"]
    ):
        # baud rate is the rate at which information is transferred (9600 bits/second)
        DataStream.__init__(self, data_channels)
        self.ser = serial.Serial(port_name, baudrate)

    def read_line(self):
        """
        returns data float
        """
        flt = self.parse_line(self.ser.readline())
        print(flt)  # for debug
        return (flt,)

    def parse_line(self, value):
        try:
            val_strn = value.decode() #try except// catch the error but don't break down please
        except Exception as e: 
            print(e)
            return 19.0
    
        val_str = val_strn.rstrip()
        
        try: 
            flt = float(val_str)
        except Exception as e: 
            print(e)
            return 19.0
        
        return flt


class RadioSerialIn(DataStream):
    """
    Class to represent Radio serial datastream object 
    TODO: Handle radio serial formatting
    """

    def __init__(self, path, data_channels=["test_data"]):
        DataStream.__init__(self, data_channels)
   
    

    def read_line(self):
        pass

    def parse_line(self):
        pass


class LogFile(DataStream):
    """
    Class to represent logfile datastream object where data can be grabbed with a single function
    TODO: Handle logfile formatting 
    """

    def __init__(self, path, data_channels=["test_data"]):
        DataStream.__init__(self, data_channels)
        self.path = path

    def read_line(self):
        with open("can5.json","r") as f:
            data = json.load(f)
            for i in data['signals']:
                print(i)
            
        # walk through csv logfile and read each line, and read each data value in the line
        # for channel in self.data_channels:
        #     # delimit with spaces, spit out data in tuple

        pass

    def parse_line(self, value):
        pass

print(LogFile.read_line(self))

class RedisDataSender(object):
    def __init__(self, data_stream_object, read_frequency_hz=5):
        self.data_stream_object = data_stream_object
        self.read_frequency_hz = read_frequency_hz
        self.data_channels = self.data_stream_object.return_data_channels()

        # initialize redis connection
        try:
            redis_instance = Redis(host="127.0.0.1", port="6379")
        except Exception as e: 
            print(e)
            return ("broken")

        # initialize redis timeseries client connection
        try:
            self.rts = Client(conn=redis_instance)
        except Exception as e: 
            print(e)
            return ("broken")
            
        
        for data_channel in self.data_channels:

            #create a data channel unless it already exists
            try:
                self.rts.create(data_channel)
            except:
                print("channel already exists")

    def grab_serial_data(self):
        while True:
            # grab data tuple from line
            tup = self.data_stream_object.read_line()
            
            # walk through all the data channels  
            for (index, data_channel) in enumerate(self.data_channels):
                # pass float into database under correct name
                self.send_to_redis_timeseries(tup[index], data_channel)
                
            time.sleep(1 / self.read_frequency_hz)  # should operate

    def send_to_redis_timeseries(self, flt, data_channel):
        self.rts.add(data_channel, "*", flt)