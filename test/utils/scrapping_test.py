import pytest
from utils.scrapping import scrap_rooms, scrap_number_ants

def test_scrap_number_ants():
    assert scrap_number_ants("fourmiliere_trois.txt") == 5
    assert scrap_number_ants("fourmiliere_cinq.txt") == 50

def test_scrap_rooms():
    assert scrap_rooms("fourmiliere_deux.txt") == {"Sv":[["S1"], None],"S1":[["S2","Sv"],None],"S2":[["Sd","S1"],None],"Sd":[["Sv","S2"],None]}
    assert scrap_rooms("fourmiliere_quatre.txt") == {"Sv":[["S1"],None],"S1":[["S2","S3","SV"],2],"S2":[["S4","S1"],None],"S3":[["S4","S1"],None],"S4":[["S2","S3","S5","S6"],2],"S5":[["Sd","S4"],None],"S6":[["Sd","S4"],None],"Sd":[["S5","S6"],None]}
