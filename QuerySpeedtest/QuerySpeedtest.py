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
from JMdictToTries import JMdictToTries
from tqdm import tqdm
import time

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.abspath(os.path.join(__file__, '../../Resources/'))
FILENAME = os.path.join(RESOURCE_DIR, 'randomWords.json')

def getDicts():
    print("\nGenerating dictionaries...\n")
    textDict = {}
    idDict = {}
    with open(os.path.join(RESOURCE_DIR, 'JMdict_e.json'), 'r', encoding='utf8') as f:
        JMdict = json.loads(f.read())
    with tqdm(total=len(JMdict)) as pbar:
        for entry in JMdict:
            id = entry['ent_seq']
            if 'k_ele' in entry:
                for kele in entry['k_ele']:
                    text = kele['keb']
                    addEntryToDict(textDict, text, id)
            for rele in entry['r_ele']:
                text = rele['reb']
                addEntryToDict(textDict, text, id)
            idDict[id] = entry
            pbar.update(1)
    return [textDict, idDict]

def addEntryToDict(dict, key, value):
    if key not in dict:
        dict[key] = []
    dict[key].append(value)

def startUtility(src="scrp"):
    print("\n---------- JMdict Query Speedtest ----------\n")
    JMdictUtils.checkForJMdict()
    JMdictUtils.checkForRandomWords()
    with open(FILENAME, 'r', encoding='utf8') as f:
        randomWords = json.loads(f.read())
    if src=='cmd':  # Trie assignment gets reversed depending on how the script is launched(???)
        idTrie, textTrie = JMdictToTries.startUtility()
    else:
        textTrie, idTrie = JMdictToTries.startUtility()
    #pdb.set_trace()
    textDict, idDict = getDicts()
    runTests(idTrie, textTrie, textDict, idDict, randomWords, repeat=8)

def runTests(idTrie, textTrie, textDict, idDict, randomWords, repeat=0):
    testIdTrie(idTrie, randomWords, repeat)
    testTextTrie(textTrie, randomWords, repeat)
    testIdDict(idDict, randomWords, repeat)
    testTextDict(textDict, randomWords, repeat)

def testTextTrie(textTrie, words, repeat=0):
    print("\nStarting text trie search...")
    oTime = time.time()
    with tqdm(total=len(words)*(repeat+1)) as pbar:
        for i in range(repeat+1):
            for word in words:
                # if 'k_ele' in word:
                #     textTrie.search(word['k_ele'][0]['keb'])
                # else:
                textTrie.search(word['r_ele'][0]['reb'])
                pbar.update(1)
    print("Completed text trie search in {} seconds".format(time.time() - oTime.__round__(2)))


def testIdTrie(idTrie, words, repeat=0):
    print("\nStarting id trie search...")
    oTime = time.time()
    with tqdm(total=len(words)*(repeat+1)) as pbar:
        for i in range(repeat+1):
            for word in words:
                idTrie.search(word['ent_seq'])
                pbar.update(1)
    print("Completed id trie search in {} seconds".format(time.time() - oTime.__round__(2)))


def testIdDict(idDict, words, repeat=0):
    print("\nStarting id dict search...")
    oTime = time.time()
    with tqdm(total=len(words)*(repeat+1)) as pbar:
        for i in range(repeat+1):
            for word in words:
                idDict.get(word['ent_seq'])
                pbar.update(1)
    print("Completed id dict search in {} seconds".format(time.time() - oTime.__round__(2)))

def testTextDict(textDict, words, repeat=0):
    print("\nStarting text dict search...")
    oTime = time.time()
    with tqdm(total=len(words)*(repeat+1)) as pbar:
        for i in range(repeat+1):
            for word in words:
                # if 'k_ele' in word:
                #     textDict.get(word['k_ele'][0]['keb'])
                # else:
                textDict.get(word['r_ele'][0]['reb'])
                pbar.update(1)
    print("Completed text dict search in {} seconds".format(time.time() - oTime.__round__(2)))



if __name__ == "__main__":
    startUtility(src='cmd')
