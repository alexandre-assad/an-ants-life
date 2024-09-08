from typing import Tuple

from networkx import shortest_path
from src.domain.anthill import Anthill
from src.domain.ant import Ant

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