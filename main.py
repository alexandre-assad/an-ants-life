from typing import Tuple
import matplotlib.pyplot as plt
from networkx import draw, spring_layout

from src.domain.anthill import Anthill
from src.domain.room import Room
from src.domain.simulation import Simulation

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
