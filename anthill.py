from utils.scrapping import scrap_number_ants, scrap_rooms

class Anthill:

    def __init__(self,anthill_file:str):
        self.n_ants = scrap_number_ants(anthill_file)
        self.rooms = scrap_rooms(anthill_file)
        # Set up all ants
        for key,values in self.rooms.items():
            self.rooms[key].append(0)
        self.rooms["Sv"][2] = self.n_ants