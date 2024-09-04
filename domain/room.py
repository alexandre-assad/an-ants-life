
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Room:
    name: str 
    index: int
    capacity: int = 1

