import os
import re

def scrap_number_ants(file:str) -> int:
    #Get the content in string format
    f = open(os.path.join("..","anthills",file), "r")
    content = f.read()
    regex_exp = r"f=(.*)\n"
    regex_str = re.search(regex_exp,content)
    return int(regex_str.group(1))

def scrap_rooms(file:str) -> dict:
    f = open(os.path.join("..","anthills",file), "r")
    content = f.read()

    #Init rooms
    rooms = {}
    rooms["Sv"] = [[],1]
    rooms["Sd"] = [[],1]

    #Now read each row and add it into rooms
    row_file = content.split("\n")[1:]
    for row in row_file:
        composent = row.split(" ")
        if len(composent) == 1:
            rooms[composent[0]] = [[],1]
        elif len(composent) == 4:
            rooms[composent[0]] = [[],int(composent[2])]
        else:
            rooms[composent[0]][0].append(composent[2])
            rooms[composent[2]][0].append(composent[0])
    return rooms