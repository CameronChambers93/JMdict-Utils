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
import JMdictUtils
from JMdictToTrie import Tries

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.abspath(os.path.join(__file__, '../../Resources/'))
JMDICT_FILENAME = os.path.join(RESOURCE_DIR, 'JMdict_e')
OUTPUT_FILENAME = os.path.join(RESOURCE_DIR, "randomWords.json")
LINE_COUNT_OFFSET = 839098      # To offset current error(?) with progress bar

def startUtility():
    JMdictUtils.checkForJMdict()
    with open(os.path.join(RESOURCE_DIR, 'JMdict_e.json'), 'r', encoding='utf8') as f:
        print("\nLoading JMdict...")
        JMdict = json.loads(f.read())
        return parseDict(JMdict)

def parseDict(jmdict):
    textTrie = Tries.TextTrie()
    idTrie = Tries.IdTrie()
    iterations = len(jmdict)
    with tqdm(total=iterations) as pbar:
        for entry in jmdict:
            if 'k_ele' in entry:
                text = entry['k_ele'][0]['keb']
            else:
                text = entry['r_ele'][0]['reb']
            textTrie.insert(text, entry['ent_seq'])
            idTrie.insert(entry['ent_seq'], entry)
            pbar.update(1)
    return {textTrie, idTrie}


if __name__ == '__name__':
    startUtility()