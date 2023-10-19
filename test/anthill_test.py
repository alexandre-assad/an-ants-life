import pytest
from anthill import Anthill

def test_init():
    anthill = Anthill("fourmiliere_quatre.txt")
    assert anthill.n_ants==10
    assert anthill.rooms["Sv"] == [["S1"],1,10]
    assert anthill.rooms["Sd"] == [["S5","S6"],10,0]


def test_set_distance_to_end():
    anthill = Anthill("fourmiliere_deux.txt")
    assert anthill.rooms == {"Sv":[["S1","Sd"],1,5,1],"S1":[["Sv","S2"],1,0,2],"S2":[["S1","Sd"],1,0,1],"Sd":[["S2","Sv"],1,0,0]}

def test_get_direction_room():
    anthill = Anthill("fourmiliere_deux.txt")
    assert anthill.rooms == {"Sv":[["S1","Sd"],1,5,1],"S1":[["S2"],1,0,2],"S2":[["Sd"],1,0,1],"Sd":[[],1,0,0]}

