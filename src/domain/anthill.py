from dataclasses import dataclass, field
import matplotlib.pyplot as plt
import numpy as np
from networkx import Graph, draw, spring_layout

from src.domain.room import Room

@dataclass
class Anthill:
    graph: Graph = field(default_factory=Graph)
    rooms: list[Room] = field(default_factory=list)

    def add_room(self, room: Room) -> None:
        if room not in self.rooms:
            self.rooms.append(room)
            self.graph.add_node(room.name)

    def add_tunnel(self, first_room: Room, second_room: Room) -> None:
        self.graph.add_edge(first_room.name, second_room.name)

    def matrix(self) -> np.ndarray:
        size = len(self.rooms)
        adj_matrix = np.zeros((size, size), dtype=int)
        for i, f_room in enumerate(self.rooms):
            for j, s_room in enumerate(self.rooms):
                if self.graph.has_edge(f_room.name, s_room.name):
                    adj_matrix[i, j] = 1
        return adj_matrix

    def display(self) -> None:
        pos = spring_layout(self.graph)
        draw(self.graph, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=15)
        plt.show()
