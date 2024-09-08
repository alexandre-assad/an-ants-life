from dataclasses import dataclass, field
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from networkx import Graph, draw, shortest_path, spring_layout


@dataclass
class Room:
    name: str
    index: int

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

class Ant:
    def __init__(self, id: str, path: list[str]) -> None:
        self.id = id
        self.path = path
        self.position: str | None = path[0] if path else None

    def move(self) -> None:
        if self.path:
            self.position = self.path.pop(0)

class Simulation:
    def __init__(self, anthill: Anthill) -> None:
        self.anthill = anthill
        self.ants: dict[str, Ant] = {}
        self.steps: list[dict[str, Tuple[str, str]]] = []

    def find_path(self, start: str, end: str) -> list[str]:
        return shortest_path(self.anthill.graph, source=start, target=end)

    def load_ants(self, number_of_ants: int) -> None:
        path = self.find_path("Sv", "Sd")
        for i in range(number_of_ants):
            self.ants[f"Ant{i + 1}"] = Ant(f"Ant{i + 1}", path[:])

    def simulate_movements(self, number_of_ants: int) -> None:
        self.load_ants(number_of_ants)

        while any(ant.path for ant in self.ants.values()):
            step: dict[str, Tuple[str, str]] = {}
            occupied_rooms: set = set()
            for ant_id, ant in self.ants.items():
                if ant.path and ant.position != "Sd":
                    next_position = ant.path[0]
                    if next_position not in occupied_rooms:
                        occupied_rooms.add(next_position)
                        step[ant_id] = (ant.position, next_position)
                        ant.move()
                        if ant.position == "Sd":
                            ant.path = []
            self.steps.append(step)

    def display_movements(self) -> None:
        for index, step in enumerate(self.steps):
            print(f"+++ Step {index + 1} +++")
            for ant_id, (position, destination) in step.items():
                if destination:
                    print(f"{ant_id} - {position} - {destination}")

def visualize_movements(simulation: Simulation, number_of_ants: int) -> None:
    fig, ax = plt.subplots()

    pos = spring_layout(simulation.anthill.graph)
    draw(simulation.anthill.graph, pos, with_labels=True, node_size=700, node_color="lightgreen", ax=ax)

    simulation.simulate_movements(number_of_ants)

    for index, step in enumerate(simulation.steps):
        ax.clear()
        draw(simulation.anthill.graph, pos, with_labels=True, node_size=700, node_color="lightgreen", ax=ax)

        for ant_id, (start, end) in step.items():
            if start and end:
                pos_start = pos[start]
                pos_end = pos[end]
                pos_mid = [(pos_start[0] + pos_end[0]) / 2, (pos_start[1] + pos_end[1]) / 2]

                ax.text(pos_mid[0], pos_mid[1], ant_id, fontsize=12, ha='center', va='center',
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

        plt.title(f"Step {index + 1}")
        plt.pause(1)

    plt.show()

def load_anthill(file_path: str) -> Tuple[Anthill, int]:
    anthill = Anthill()
    number_of_ants = 0
    with open(file_path) as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line.startswith("f="):
                number_of_ants = int(line.split('=')[1])
            elif ' - ' in line:
                room1, room2 = line.split(' - ')
                anthill.add_tunnel(Room(room1, len(anthill.rooms)), Room(room2, len(anthill.rooms)))
            else:
                anthill.add_room(Room(line, len(anthill.rooms)))
    return anthill, number_of_ants

def main() -> None:
    anthill, number_of_ants = load_anthill("anthills/fourmiliere_trois.txt")
    simulation = Simulation(anthill)
    visualize_movements(simulation, number_of_ants)

if __name__ == "__main__":
    main()
