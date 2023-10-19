import pytest
from utils.scrapping import scrap_rooms, scrap_number_ants

def test_scrap_number_ants():
    assert scrap_number_ants("fourmiliere_trois.txt") == 5
    assert scrap_number_ants("fourmiliere_cinq.txt") == 50

def test_scrap_rooms():
    assert scrap_rooms("fourmiliere_deux.txt") == {"Sv":[["S1","Sd"], 1],"S1":[["Sv","S2"],1],"S2":[["S1","Sd"],1],"Sd":[["S2","Sv"],1]}
    assert scrap_rooms("fourmiliere_quatre.txt") == {"Sv":[["S1"],1],"S1":[["Sv","S2","S3"],2],"S2":[["S1","S4"],1],"S3":[["S4","S1"],1],"S4":[["S3","S2","S5","S6"],2],"S5":[["S4","Sd"],1],"S6":[["S4","Sd"],1],"Sd":[["S5","S6"],1]}
