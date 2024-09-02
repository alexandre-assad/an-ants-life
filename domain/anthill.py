from dataclasses import dataclass

from .room import Room

Connection = tuple[Room, Room]

@dataclass
class Anthill:
    number_of_ants: int
    rooms: list[Room]
    connections: list[Connection]

    @property
    def connections_map(self) -> dict[]