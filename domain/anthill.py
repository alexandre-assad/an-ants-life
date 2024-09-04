from dataclasses import dataclass
from functools import cached_property
from multiprocessing import connection
from typing import List

from .room import Room

Connection = tuple[Room, Room]

@dataclass
class Anthill:
    number_of_ants: int
    rooms: list[Room]
    connections: list[Connection]

    @cached_property
    def connections_map(self) -> dict[Room, List[Room]]:
        connection_map = {}
        for connection in self.connections:
            first_room, second_room = connection[0], connection[1]

            if first_room not in connection_map:
                connection_map[first_room] = [second_room]
            else:
                connection_map[first_room].append(second_room)

        return connection_map
    
    @property
    def adjacency_matrix(self) -> List[List[int]]:
        matrix = []
        self.rooms.sort(key = lambda x: x.index)
        for room in self.rooms:
            sub_matrix = [0] * len(self.rooms)
            for linked_room in self.connections_map[room]:
                sub_matrix[linked_room.index] = 1
            matrix.append(sub_matrix)
        return matrix
    

    def ant_journey(self) -> None:
        pass