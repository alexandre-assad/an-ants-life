from dataclasses import dataclass
import os
import re
from typing import Dict, List

from ..domain.anthill import Anthill
from domain.room import Room

Connection = tuple[Room, Room] #single key

def find_number_ants(file_content: str) -> int:
    regex_exp = r"f=(.*)\n"
    regex_str = re.search(regex_exp,file_content)
    if not regex_str or not regex_str.group(1):
        raise ValueError()
    
    return int(regex_str.group(1))

def find_room(file_row: str) -> Room:
    pass 

def find_connections(file_row: str, rooms: List[Room]) -> Connection:
    row_split = file_row.split(" ")
    first_room_name, second_room_name = row_split[0], row_split[2]
    first_room, second_room = infer_room_by_name(first_room_name, rooms),infer_room_by_name(second_room_name, rooms)
    return first_room, second_room


def infer_room_by_name(name: str, rooms: list[Room]) -> Room:
    for room in rooms:
        if room.name == name:
            return room
    raise ValueError()


def parse_anthill_from_file(file_path: str) -> Anthill:
    file = open(os.path.join("..","anthills",file_path) , "r")
    file_content = file.read()

    rooms = []
    connections = []
    number_ants = find_number_ants(file_content)

    #Now read each row and add it into rooms
    file_by_row = file_content.split("\n")[1:]
    for row in file_by_row:
        # #Init room 
        # if len(composent) == 1:
        #     rooms[composent[0]] = [[],1]
        # elif len(composent) == 4:
        #     rooms[composent[0]] = [[],int(composent[2])]
        # else:
        #     #Connections with subfunction
        #     rooms[composent[0]][0].append(composent[2])
            # rooms[composent[2]][0].append(composent[0])
        is_link = '-' in row 
        is_room = len(row.split(" ")) == 1 or '{' in row
        if is_room:
            rooms.append(find_room(row))
        elif is_link:
            connections.append(find_connections(row, rooms))
        else: 
            raise ValueError()
    return Anthill(rooms=rooms, number_of_ants = number_ants,connections = connections)


