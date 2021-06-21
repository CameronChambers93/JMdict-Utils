import pdb
import math
import random
from xml.etree import ElementTree as ET 
import re
import time
import copy
import json
import os
from tqdm import tqdm

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(CURRENT_DIR, 'JMdict_e')

def parse_rele(elements, new_ele):
    for ele in elements:
        if ele.tag.lower() == 'reb':
            if new_ele['r_ele'] == '':
                new_ele['r_ele'] = ele.text

def parse_kele(elements, new_ele):
    for ele in elements:
        if ele.tag.lower() == 'keb':
            if new_ele['k_ele'] == '':
                new_ele['k_ele'] = ele.text

def saveRandomWords():
    f = ET.iterparse(FILENAME)
    count = math.floor(random.random() * 300)
    words = []
    for event, elements in tqdm(f):
        if event == 'end' and elements.tag == 'entry' and count > 100:
            new_ele = {'r_ele': '', 'k_ele': ''}
            for ele in elements.iter():
                if ele.tag == "k_ele":
                    parse_kele(ele, new_ele)
                elif ele.tag == "r_ele":
                    parse_rele(ele, new_ele)
            if len(new_ele['k_ele']) > 6 or (new_ele['k_ele'] == '' and len(new_ele['r_ele']) > 6):
                if new_ele['k_ele'] == '':
                    words.append(new_ele['r_ele'])
                else:
                    words.append(new_ele['k_ele'])
                count = 0
        count += math.floor(random.random() * 5)
    return words

def startUtility():
    words = saveRandomWords()
    file = open('randomWords.json', 'w', encoding='utf-8')
    print("Saving file...")
    json.dump(words, file, indent=2, ensure_ascii=False)
    print("Finished saving to file 'randomWords.json'")
    file.close()

if __name__ == "__main__":
    startUtility()