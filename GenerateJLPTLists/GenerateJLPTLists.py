from tqdm.std import tqdm
from QuerySpeedtest import QuerySpeedtest
import JMdictUtils
import os
import csv
import pdb
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.abspath(os.path.join(__file__, '../../Resources/'))
OUTPUT_FILENAME = os.path.join(RESOURCE_DIR, 'idsByJLPT.json')

JLPT1_FILENAME = 'vocabulary_65001.csv'
JLPT2_FILENAME = 'vocabulary_65002.csv'
JLPT3_FILENAME = 'vocabulary_65003.csv'
JLPT4_FILENAME = 'vocabulary_65004.csv'
JLPT5_FILENAME = 'vocabulary_65005.csv'

# Used for words which differ in spelling from its entry in the JMdict
WORD_EXCEPTIONS = json.loads(open(os.path.join(CURRENT_DIR, 'wordExceptions.json'), encoding='utf8').read())

JLPT = [JLPT1_FILENAME, JLPT2_FILENAME, JLPT3_FILENAME, JLPT4_FILENAME, JLPT5_FILENAME]

TEXT_DICT, ID_DICT = None, None

def startUtility():
    print("\n-------------- Generate List of Words by JLPT --------------")
    getDicts()
    jlpt = getJLPT()
    saveJLPT(jlpt)

def getTotalWords():
    total = 0
    for jlpt in JLPT:
        with open(os.path.join(CURRENT_DIR, jlpt), encoding='utf8') as f:
            total = total + len(f.readlines())
    return total

def getJLPT():
    jlpt = {}
    print("\nParsing JLPT files, please wait...\n")
    with tqdm(total=getTotalWords()) as pbar:
        for i in range(len(JLPT)):
            words = []
            with open(os.path.join(CURRENT_DIR, JLPT[i]), encoding='utf8') as f:
                reader = csv.reader(f, delimiter=',')
                for row in reader:
                    common, uncommon = row[0], row[1]
                    ids = getIds(common, uncommon)
                    if ids == None:
                        addExceptions(words, common)
                        continue
                    processEntry(words, ids, common, uncommon)
                    pbar.update(1)
            jlpt[i+1] = words
    return jlpt

def processEntry(words, ids, common, uncommon):
    found = False
    for id in ids:
        entry = ID_DICT.get(id)
        if checkEntryForMatch(common, uncommon, entry):
            found = True
            words.append(id)
    if not found:
        Exception("Could not process word", ids, common, uncommon)
        # pdb.set_trace()

def addExceptions(words, common):
    if common in WORD_EXCEPTIONS:
        for id in WORD_EXCEPTIONS.get(common)['ids']:
            words.append(id)

def getIds(common, uncommon):
    ids = TEXT_DICT.get(common)
    if ids == None:
        ids = TEXT_DICT.get(uncommon)

def saveJLPT(jlpt):
    print("\nSaving file...\n")
    with open(OUTPUT_FILENAME, 'w', encoding='utf8') as f:
        json.dump(jlpt, f, indent=2, ensure_ascii=False)
    print("File saved to {}".format(OUTPUT_FILENAME))

def getDicts():
    global TEXT_DICT, ID_DICT
    TEXT_DICT, ID_DICT = QuerySpeedtest.getDicts()

def checkEntryForMatch(common, uncommon, entry):
    if containsKanji(common) or uncommon == '':
        for rele in entry['r_ele']:
            if uncommon == rele['reb'] or (uncommon == '' and common == rele['reb']):
                return True
    else:
        if 'k_ele' in entry:
            for kele in entry['k_ele']:
                if uncommon == kele['keb']:
                    return True
    return False

def containsKanji(text):
    for char in text:
        if ord(char) > 12543:   # A crude check for kanji, but shouldn't be a problem
            return True
    return False

if __name__=='__main__':
    startUtility()