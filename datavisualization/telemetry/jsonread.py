import json 

with open ("can5.json","r") as f:
    data = json.load(f)
    for i in data['signals']:
        print(i)    
            
f.close()