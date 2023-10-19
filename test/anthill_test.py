import pytest
from anthill import Anthill

def test_init():
    anthill = Anthill("fourmiliere_quatre.txt")
    assert anthill.n_ants==10
    assert anthill.rooms["Sv"] == [["S1"],1,10]