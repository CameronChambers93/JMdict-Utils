from xml.etree import ElementTree as ET 
import re
import copy
import json
import os
from tqdm import tqdm
import readchar
import pdb
import requests
import gzip
import shutil
from JMdictToJSON import JMdictToJSON
from RandomWordsToJSON import RandomWordsToJSON
from QuerySpeedtest import QuerySpeedtest
from GenerateJLPTLists import GenerateJLPTLists
import sys

UTILS = [{'name': 'Generate Random words', 'utility': RandomWordsToJSON},
            {'name': 'Output JSON to file', 'utility': JMdictToJSON},
            {'name': 'JMdict Query Speedtest', 'utility': QuerySpeedtest},
            {'name': 'Generate List of Words by JLPT', 'utility': GenerateJLPTLists},
            ]
UTIL_CHOICE = 0

UP_ARROW = "\x1b\x5b\x41"
DOWN_ARROW = "\x1b\x5b\x42"
ENTER = "\x0d"

JMDICT_URL = "http://ftp.edrdg.org/pub/Nihongo/JMdict_e.gz"

RESOURCE_DIR = os.path.join(os.path.curdir, 'Resources/')

def getArgs():
    args = []
    if len(sys.argv) > 0:
        for i in range(1, len(sys.argv)):
            option = re.search(r'-[-]*([a-z-]*)(=([a-z0-9]*))*', sys.argv[i])
            if option == None:
                raise Exception(sys.argv[i])
            name = option.group(1)
            value = option.group(3)
            args.append({'name': name, 'value': value})
    return args

def clearScreen():
    os.system('cls')

def printMenu():
    print('\n--------------- JMdict Utilities ---------------\n')
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
        UTIL_CHOICE = (UTIL_CHOICE - 1) % len(UTILS)
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

def checkForDownload():
    if 'JMdict_e' not in os.listdir('Resources'):
        downloadJMdict()
        unpackJMdict()
        deleteJMdictZip()

def downloadJMdict():
    if 'JMdict_e.gz' not in os.listdir('Resources'):
        f = open("Resources/JMdict_e.gz", 'wb')
        response = requests.get(JMDICT_URL, stream=True)
        total = response.headers.get('content-length')
        total = int(total)
        print("\nDownloading JMdict.gz...")
        with tqdm(total=total) as pbar:
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded = len(data)
                f.write(data)
                pbar.update(downloaded)
                #print('\r[{}{}]'.format('█' * done, '.' * (50-done)))

def _reader_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)

def getGzipNewlineCount():
    f = gzip.open('Resources/JMdict_e.gz', 'rb')
    f_gen = _reader_generator(f.read)
    return sum(buf.count(b'\n') for buf in f_gen)
    
def deleteJMdictZip():
    try:
        os.remove("Resources/JMdict_e.gz")
    except Exception as e:
        print("Error deleting 'JMdict_e.gz'")


def unpackJMdict():
    linecount = getGzipNewlineCount()
    print("\nUnpacking JMdict_e.gz\n")
    with open('Resources/JMdict_e', 'wb') as f_out:
        with gzip.open('Resources/JMdict_e.gz', 'rb') as f_in:
            with tqdm(f_in, total=linecount) as pbar:
                for line in f_in:
                    try:
                        f_out.write(line)
                        pbar.update(1)
                    except UnicodeDecodeError as e:
                        pdb.set_trace()


def checkForJMdict():
    if 'JMdict_e.json' not in os.listdir(RESOURCE_DIR):
        print("Requires 'JMdict_e.json' to run, press any key to run 'JMdictToJSON'")
        readchar.readkey()
        JMdictToJSON.startUtility()

def getJMdict():
    checkForJMdict()
    with open(os.path.join(RESOURCE_DIR, 'JMdict_e.json'), encoding='utf8') as f:
        return json.loads(f.read())

def checkForRandomWords():
    if 'randomWords.json' not in os.listdir(RESOURCE_DIR):
        print("Requires 'randomWords.json' to run, press any key to run 'RandomWordsToJSON'")
        readchar.readkey()
        RandomWordsToJSON.startUtility()


if __name__ == "__main__":
    showMenu()
