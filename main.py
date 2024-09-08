from dataclasses import dataclass
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple, Optional

class Fourmiliere:
    def __init__(self) -> None:
        self.graph: nx.Graph = nx.Graph()
        self.salles: List[str] = []
        self.salle_indices: Dict[str, int] = {}
        self.matrice_adjacence: Optional[np.ndarray] = None
    
    def ajouter_salle(self, salle: str) -> None:
        if salle not in self.salles:
            index: int = len(self.salles)
            self.salles.append(salle)
            self.salle_indices[salle] = index
            self.graph.add_node(salle)
    
    def ajouter_tunnel(self, salle1: str, salle2: str) -> None:
        self.graph.add_edge(salle1, salle2)
    
    def generer_matrice_adjacence(self) -> None:
        taille: int = len(self.salles)
        self.matrice_adjacence = np.zeros((taille, taille), dtype=int)
        for salle1 in self.salles:
            for salle2 in self.salles:
                if self.graph.has_edge(salle1, salle2):
                    i: int = self.salle_indices[salle1]
                    j: int = self.salle_indices[salle2]
                    self.matrice_adjacence[i][j] = 1
    
    def afficher_matrice_adjacence(self) -> None:
        if self.matrice_adjacence is None:
            self.generer_matrice_adjacence()
        print("Matrice d'adjacence :")
        print(self.matrice_adjacence)
    
    def afficher_fourmiliere(self) -> None:
        pos: Dict[str, Tuple[float, float]] = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=15)
        plt.show()

class Fourmi:
    def __init__(self, id: str, chemin: List[str]) -> None:
        self.id: str = id
        self.chemin: List[str] = chemin
        self.position: Optional[str] = chemin[0] if chemin else None
    
    def deplacer(self) -> None:
        if self.chemin:
            self.position = self.chemin.pop(0)

class Simulation:
    def __init__(self, fourmiliere: Fourmiliere) -> None:
        self.fourmiliere: Fourmiliere = fourmiliere
        self.fourmis: Dict[str, Fourmi] = {}
        self.etapes: List[Dict[str, Tuple[str, str]]] = []
    
    def trouver_chemin(self, start: str, end: str) -> List[str]:
        return nx.shortest_path(self.fourmiliere.graph, source=start, target=end)
    
    def charger_fourmis(self, nombre_fourmis: int) -> None:
        chemin: List[str] = self.trouver_chemin("Sv", "Sd")
        for i in range(nombre_fourmis):
            self.fourmis[f"F{i+1}"] = Fourmi(f"F{i+1}", chemin[:])
    
    def simuler_deplacements(self, nombre_fourmis: int) -> None:
        self.charger_fourmis(nombre_fourmis)
        
        while any(fourmi.chemin for fourmi in self.fourmis.values()):
            etape: Dict[str, Tuple[str, str]] = {}
            salle_occupees: set = set()
            for id_fourmi, fourmi in self.fourmis.items():
                if fourmi.chemin and fourmi.position != "Sd":
                    next_position: str = fourmi.chemin[0]
                    if next_position not in salle_occupees:
                        salle_occupees.add(next_position)
                        etape[id_fourmi] = (fourmi.position, next_position)
                        fourmi.deplacer()
                        if fourmi.position == "Sd":
                            fourmi.chemin = []  # Vide le chemin pour arrêter la fourmi à Sd
            self.etapes.append(etape)

    def afficher_deplacements(self) -> None:
        for index, etape in enumerate(self.etapes):
            print(f"+++E{index + 1}+++")
            for id_fourmi, (position, destination) in etape.items():
                if destination:  # Affiche seulement les déplacements valides
                    print(f"{id_fourmi} - {position} - {destination}")

def visualiser_deplacements(simulation: Simulation) -> None:
    fig, ax = plt.subplots()

    pos: Dict[str, Tuple[float, float]] = nx.spring_layout(simulation.fourmiliere.graph)  # Obtenir la disposition des nœuds
    nx.draw(simulation.fourmiliere.graph, pos, with_labels=True, node_size=700, node_color="lightgreen", ax=ax)
    
    nombre_fourmis: int = len(simulation.fourmis)
    simulation.simuler_deplacements(nombre_fourmis)
    
    # Visualiser les déplacements
    for index, etape in enumerate(simulation.etapes):
        ax.clear()
        nx.draw(simulation.fourmiliere.graph, pos, with_labels=True, node_size=700, node_color="lightgreen", ax=ax)
        
        # Ajouter des annotations pour représenter les fourmis par F(n)
        for id_fourmi, (start, end) in etape.items():
            if start and end:
                # Calculer une position intermédiaire entre start et end pour placer l'annotation
                pos_start: Tuple[float, float] = pos[start]
                pos_end: Tuple[float, float] = pos[end]
                pos_mid: Tuple[float, float] = [(pos_start[0] + pos_end[0]) / 2, (pos_start[1] + pos_end[1]) / 2]
                
                # Placer l'annotation à mi-chemin
                ax.text(pos_mid[0], pos_mid[1], id_fourmi, fontsize=12, ha='center', va='center',
                        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
        
        plt.title(f"Étape {index + 1}")
        plt.pause(1)  # Pause pour montrer les étapes une par une

    plt.show()

def charger_fourmiliere(fichier_fourmiliere: str) -> Tuple[Fourmiliere, int]:
    fourmiliere: Fourmiliere = Fourmiliere()
    nombre_fourmis: int = 0
    with open(fichier_fourmiliere, 'r') as file:
        lignes: List[str] = file.readlines()
        for ligne in lignes:
            ligne = ligne.strip()
            if ligne.startswith("f="):
                nombre_fourmis = int(ligne.split('=')[1])
            elif ' - ' in ligne:
                salle1, salle2 = ligne.split(' - ')
                fourmiliere.ajouter_tunnel(salle1, salle2)
            else:
                fourmiliere.ajouter_salle(ligne)
    return fourmiliere, nombre_fourmis

def main() -> None:
    fourmiliere, _ = charger_fourmiliere("data/fourmiliere_trois.txt")
    simulation = Simulation(fourmiliere)
    visualiser_deplacements(simulation)

