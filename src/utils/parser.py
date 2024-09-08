import os
import re
from typing import List

from src.domain.anthill import Anthill
from src.domain.room import Room


Connection = tuple[Room, Room]  # single key


def find_number_ants(file_content: str) -> int:
    regex_exp = r"f=(.*)\n"
    regex_str = re.search(regex_exp, file_content)
    if not regex_str or not regex_str.group(1):
        raise ValueError()
    return int(regex_str.group(1))


def find_room(file_row: str, room_index: int) -> Room:
    name = file_row.split(" ")[0]
    if "{" in file_row:
        capacity = int(file_row.split(" ")[2])
        return Room(name=name, index=room_index, capacity=capacity)
    return Room(name, room_index)


def find_connections(file_row: str, rooms: List[Room]) -> Connection:
    row_split = file_row.split(" ")
    first_room_name, second_room_name = row_split[0], row_split[2]
    first_room, second_room = infer_room_by_name(
        first_room_name, rooms
    ), infer_room_by_name(second_room_name, rooms)
    return first_room, second_room


def infer_room_by_name(name: str, rooms: list[Room]) -> Room:
    for room in rooms:
        if room.name == name:
            return room
    raise ValueError()


def parse_anthill_from_file(file_path: str) -> Anthill:
    file = open(os.path.join("..", "anthills", file_path), "r")
    file_content = file.read()

    rooms = []
    connections = []
    number_ants = find_number_ants(file_content)

    rooms.append(Room("Sv", 0, number_ants))
    room_index = 0
    file_by_row = file_content.split("\n")[1:]
    for row in file_by_row:
        is_link = "-" in row
        is_room = len(row.split(" ")) == 1 or "{" in row
        if is_room:
            rooms.append(find_room(row, room_index))
            room_index += 1
        elif is_link:
            connections.append(find_connections(row, rooms))
        else:
            raise ValueError()
    rooms.append(Room("Sd", room_index, number_ants))
    return Anthill(rooms=rooms, number_of_ants=number_ants, connections=connections)
