import os
import re

def scrap_number_ants(file:str) -> int:
    #Get the content in string format
    f = open(os.path.join("..","anthills",file), "r")
    content = f.read()
    regex_exp = r"f=(.*)\n"
    regex_str = re.search(regex_exp,content)
    return int(regex_str.group(1))

def scrap_rooms(file:str) -> list:
    return []