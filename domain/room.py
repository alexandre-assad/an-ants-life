
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Room:
    name: str 
    capacity: int = 1

