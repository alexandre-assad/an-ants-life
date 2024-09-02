from dataclasses import dataclass
from typing import List

from .room import Room

Connection = tuple[Room, Room]

@dataclass
class Anthill:
    number_of_ants: int
    rooms: list[Room]
    connections: list[Connection]

    @property
    def connections_map(self) -> dict[Room, List[Room]]:
        connection_map = {}
        for connection in self.connections:
            first_room, second_room = connection[0], connection[1]

            if first_room not in connection_map:
                connection_map[first_room] = [second_room]
            else:
                connection_map[first_room].append(second_room)

            if second_room not in connection_map:
                connection_map[second_room] = [first_room]
            else:
                connection_map[second_room].append(first_room)

        return connection_map