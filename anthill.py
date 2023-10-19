from utils.scrapping import scrap_number_ants, scrap_rooms

class Anthill:

    def __init__(self,anthill_file:str):
        # Set up the anthill
        self.n_ants: int = scrap_number_ants(anthill_file)
        self.rooms: dict = scrap_rooms(anthill_file)   #FORMAT : self.rooms["ROOM"] = [[room_linked_1,room_linked_2],capacity,ant_in_room]
        self.rooms["Sd"][1] = self.n_ants

        # Set up all ants
        for key,values in self.rooms.items():
            self.rooms[key].append(0)
        self.rooms["Sv"][2] = self.n_ants


    def get_direction_room(self):
        #We want to have a direction, so we will think about "level", the distance from a room to the dormitory
        pass