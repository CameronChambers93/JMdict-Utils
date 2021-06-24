import pdb
import math
import random
from xml.etree import ElementTree as ET 
import re
import time
import copy
import json
import os
import readchar
from tqdm import tqdm
import JMdictUtils

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.abspath(os.path.join(__file__, '../../Resources/'))
JMDICT_FILENAME = os.path.join(RESOURCE_DIR, 'JMdict_e.json')
OUTPUT_FILENAME = os.path.join(RESOURCE_DIR, "randomWords.json")
LINE_COUNT_OFFSET = 839098      # To offset current error(?) with progress bar

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

def getRandomWords(min_word_length = 2):
    count = 0
    with open(JMDICT_FILENAME, 'r', encoding='utf8') as f:
        jmdict = json.loads(f.read())
    words = []
    with tqdm(total=len(jmdict)) as pbar:
        for word in jmdict:
            if count > 10:
                if 'k_ele' in word:
                    if len(word['k_ele'][0]['keb']) >= min_word_length:
                        words.append(word)
                        count = 0
                elif len(word['r_ele'][0]['reb']) >= min_word_length:
                        words.append(word)
                        count = 0
            count += math.floor(random.random() * 5)
            pbar.update(1)
    return words

def getMinWordLength():
    length = input("\nMinimum word length (default = 0): ")
    try:
        return int(length)
    except:
        return 0

def startUtility(min_word_length=None):
    JMdictUtils.checkForDownload()
    if min_word_length == None:
        min_word_length = getMinWordLength()
    print("\nGenerating random words...\n")
    words = getRandomWords(min_word_length)
    saveWords(words)

def saveWords(words):
    file = open(OUTPUT_FILENAME, 'w', encoding='utf-8')
    print("\nSaving {} words to file...\n".format(len(words)))
    json.dump(words, file, indent=2, ensure_ascii=False)
    print("Finished saving to {}".format(OUTPUT_FILENAME))
    file.close()

def getArgs():
    min_word_length = 0
    args = JMdictUtils.getArgs()
    for arg in args:
        name = arg['name']
        value = arg['value']
        if name == 'min-word-length' or name == 'm':
            min_word_length = int(value)
        else:
            raise Exception(arg)
    return min_word_length
    

if __name__ == "__main__":
    min_word_length = getArgs()
    startUtility(min_word_length)