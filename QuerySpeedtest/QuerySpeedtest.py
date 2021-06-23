import os
import pdb
from random import random
import sys
from os import path
import json
import JMdictUtils
import readchar
from JMdictToJSON import JMdictToJSON
from RandomWordsToJSON import RandomWordsToJSON
from JMdictToTrie import JMdictToTrie
from tqdm import tqdm
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.abspath(os.path.join(__file__, '../../Resources/'))
FILENAME = os.path.join(RESOURCE_DIR, 'randomWords.json')

def getDicts():
    textDict = {}
    idDict = {}
    with open(os.path.join(RESOURCE_DIR, 'JMdict_e.json'), 'r', encoding='utf8') as f:
        JMdict = json.loads(f.read())
    for entry in JMdict:
        if 'k_ele' in entry:
            text = entry['k_ele'][0]['keb']
        else:
            text = entry['r_ele'][0]['reb']
        textDict[text] = True
        idDict[entry['ent_seq']] = True
    return [textDict, idDict]


def startUtility():
    print("\n---------- JMdict Query Speedtest ----------\n")
    JMdictUtils.checkForJMdict()
    JMdictUtils.checkForRandomWords()
    with open(FILENAME, 'r', encoding='utf8') as f:
        randomWords = json.loads(f.read())
    idTrie, textTrie = JMdictToTrie.startUtility()
    textDict, idDict = getDicts()
    runTests(idTrie, textTrie, textDict, idDict, randomWords, repeat=4)

def runTests(idTrie, textTrie, textDict, idDict, randomWords, repeat=0):
    for i in range(repeat+1):
        testIdTrie(idTrie, randomWords, repeat=8)
        testTextTrie(textTrie, randomWords, repeat=8)
        testIdDict(idDict, randomWords, repeat=8)
        testTextDict(textDict, randomWords, repeat=8)

def testTries(textTrie, idTrie, words, repeat=0):
    print("\nStarting tries search...")
    oTime = time.time()
    with tqdm(total=len(words)*(repeat+1)) as pbar:
        for i in range(repeat+1):
            for word in words:
                idTrie.search(id)
                pbar.update(1)
    print("Completed tries search in {} seconds".format(time.time() - oTime.__round__(2)))

def testTextTrie(textTrie, words, repeat=0):
    print("\nStarting text trie search...")
    oTime = time.time()
    with tqdm(total=len(words)*(repeat+1)) as pbar:
        for i in range(repeat+1):
            for word in words:
                textTrie.search(word)
                pbar.update(1)
    print("Completed text trie search in {} seconds".format(time.time() - oTime.__round__(2)))

if __name__ == "__main__":
    startUtility()
