from xml.etree import ElementTree as ET 
import re
import copy
import json
import os
from tqdm import tqdm
import readchar
import pdb
import JMdictToJSON
import RandomWordsToJSON

UTILS = [{'name': 'Random words', 'utility': RandomWordsToJSON},
            {'name': 'Output JSON to file', 'utility': JMdictToJSON}]
UTIL_CHOICE = 0

UP_ARROW = "\x1b\x5b\x41"
DOWN_ARROW = "\x1b\x5b\x42"
ENTER = "\x0d"

# def xml_parser():
#     """ Parse the large XML file using generator to speed up load time """
#     f = ET.iterparse(FILE)
#     DATA = []
#     # main_element = f.getroot()
#     for event, elements in tqdm(f):
#         if event == 'end' and elements.tag == 'entry':
#             new_ele = copy.deepcopy(TEMPLATE)
#             for ele in elements.iter():
#                 if ele.tag == "ent_seq":
#                     parse_ent_seq(ele, new_ele)
#                 elif ele.tag == "r_ele":
#                     parse_rele(ele, new_ele)
#                 elif ele.tag == "k_ele":
#                     parse_kele(ele, new_ele)
#                 elif ele.tag == "sense":
#                     parse_sense(ele, new_ele)
#             DATA.append(new_ele)
#     return {"words": DATA}

def xml_to_json():
    """ Convert xml to json and save to file """
    file = open("JMdict_e.json", "w", encoding="utf8")
    print("Beginning conversion of JMdict_e")
    json.dump(xml_parser(), file, indent=2, ensure_ascii=False)
    print("Conversion finished")
    print("Saving to file...")
    file.close()

def clearScreen():
    os.system('cls')

def printMenu():
    print('JMdict Utilities\n')
    count = 0
    for util in UTILS:
        if count == UTIL_CHOICE:
            print('>>> {util}'.format(util = util['name']))
        else:
            print(util['name'])
        count += 1

def getInput():
    print('\nPlease select a utility using ^, v, and enter')
    return readchar.readkey()

def startUtility():
    UTILS[UTIL_CHOICE]['utility'].startUtility()

def processInput(input):
    global UTIL_CHOICE
    if input == UP_ARROW:
        UTIL_CHOICE = (UTIL_CHOICE + 1) % len(UTILS)
    elif input == DOWN_ARROW:
        UTIL_CHOICE = (UTIL_CHOICE + 1) % len(UTILS)
    elif input == ENTER:
        return startUtility()
    showMenu()

def showMenu():
    clearScreen()
    printMenu()
    input = getInput()
    processInput(input)

if __name__ == "__main__":
    showMenu()