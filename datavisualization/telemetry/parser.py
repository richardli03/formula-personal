"""
Entrypoint app file

Objective: use cantools to decrypt bits coming in from the USB. 

Args:
    takes in dbc file and CAN bytes
    

Returns:
    Python objects // data in a way that python can use (dictionaries, classes, etc. feedable into redis)
    In other words, the data that we want to display. 
"""


import ast
import csv
import can
import cantools
import json 
import serial
import time
from redis import Redis
from redistimeseries.client import Client



def decode_csv(dbc, can_csv):
    db = cantools.database.load_file(dbc) #gets db file used to decode messages
    final_list = [] #initializes list that will contain the data in the right format
    decoded_file = open("decoded_can.json", "w")
    i = 0
    
    with open (r'{}'.format(can_csv), newline='') as can: #opens csv file that needs to be decoded
        csv_file = csv.reader(can, delimiter=' ') #reads csv file
        for row in csv_file: #for each row in the csv file 
            for string in row: #for each value in the row divide it up based on commas to separate the values that we need
                temp_list = string.split(',')
                temp_list = list(filter(None, temp_list)) #filters out empty values 
                int_list = [] #list with each value as an int
                for value in temp_list: #converts each value from str to int
                    x = int(value)
                    int_list.append(x)
                final_list.append(int_list)



    """
    for data in final_list: #takes each list inside this list
        i += 1
        #removes id and assigns it to can_id
        can_id = data.pop(0) 
        
         #decodes the message using the dbc
        decoded = db.decode_message(can_id, data)
        
        #gets all the information about the signal like name, length etc
        x = db.get_message_by_frame_id(can_id) 
        
        decoded_dict = {
                "time_start": i,
                "time_end": i + 0.1,
                "id":can_id, 
                "name":x.name, 
                "length":x.length, 
                "signals":decoded}
        
        # Use double quotes instead of python dictionary single quotes
        dict = json.dumps(decoded_dict)
        decoded_file.write(str(dict) + '\n')
        time.sleep(5)

    """



if __name__ == "__main__":
    decode_csv("dash.dbc","can5.csv")