"""
Entrypoint app file

Objective: use cantools to decrypt bits coming in from the USB. 

Args:
    takes in dbc file and CAN bytes
    

Returns:
    Python objects // data in a way that python can use (dictionaries, classes, etc. feedable into redis)
    In other words, the data that we want to display. 
"""


import argparse
import ast
import csv
import can
import cantools
import sys
import json


#Takes stdin and decodes it
def decode_csv_live(dbc):
    i = 0
    db = cantools.database.load_file(dbc) #gets db file used to decode messages
    for line in sys.stdin:
        line = line.rstrip()
        if 'Exit' == line.rstrip():
            print("Done")
            break
        temp_list = line.split(',')
        temp_list = list(filter(None, temp_list)) #filters out empty values 
        data = [int(x) for x in temp_list]
        if len(data) == 0:
            break
        can_id = data.pop(0) #removes id and assigns it to can_id
        decoded = db.decode_message(can_id, data) #decodes the message using the dbc
        x = db.get_message_by_frame_id(can_id) #gets all the information about the signal like name, length ect
        decoded_dict = {
                "time_start": i,
                "time_end": i + 0.1,
                "id":can_id, 
                "name":x.name, 
                "length":x.length, 
                "signals":decoded}
        print(decoded_dict)

def decode_csv(dbc, can_csv, new_file):
    db = cantools.database.load_file(dbc) #gets db file used to decode messages
    final_list = [] #initializes list that will contain the data in the right format
    decoded_file = open("{}".format(new_file), "w")
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
    for data in final_list: #takes each list inside this list
        i += 1
        can_id = data.pop(0) #removes id and assigns it to can_id
        decoded = db.decode_message(can_id, data) #decodes the message using the dbc
        x = db.get_message_by_frame_id(can_id) #gets all the information about the signal like name, length etc
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
        

#CLI
parser = argparse.ArgumentParser()
parser.add_argument('--json', help="decoded file in .txt format", type=str)
parser.add_argument('--dbc', help="database file in .dbc format", type=str)
parser.add_argument('--csv', help="csv file to be decoded", type=str)
parser.add_argument('--name', help="name of CAN message", type=str)
parser.add_argument('--new_file', help="what you want the name of the decoded file to be", type=str)
parser.add_argument('--signal', help="signal in CAN Data Frame", type=str)
parser.add_argument('--value', help="value of signal in CAN Data frame", type=int)
parser.add_argument('--time_start', help="start time that you are looking for", type = int)
parser.add_argument('--time_end', help="end time that you are looking for", type = int)
parser.add_argument('--id', help="id of CAN message", type = int)

parser.add_argument("--decode_csv_live", help="takes values separated by commas and converts it into json form. Type 'Exit' to stop. Only takes in dbc", action='store_true')
parser.add_argument("--decode_csv", help="decodes csv file using a dbc, takes in csv, dbc and name you want for decoded file", action='store_true')

args = parser.parse_args()
if args.decode_csv:
    decode_csv(args.dbc, args.csv, args.new_file)
elif args.decode_csv_live:
    decode_csv_live(args.dbc)