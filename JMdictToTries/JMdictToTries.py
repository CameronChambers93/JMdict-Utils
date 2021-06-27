import json
import os
from tqdm import tqdm
import JMdictUtils
from JMdictToTries import Tries

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../Resources/'))
JMDICT_FILENAME = os.path.join(RESOURCE_DIR, 'JMdict_e')
OUTPUT_FILENAME = os.path.join(RESOURCE_DIR, "randomWords.json")

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
                for kele in entry['k_ele']:
                    textTrie.insert(kele['keb'], entry['ent_seq'])
            for rele in entry['r_ele']:
                textTrie.insert(rele['reb'], entry['ent_seq'])
            idTrie.insert(entry['ent_seq'], entry)
            pbar.update(1)
    return {textTrie, idTrie}


if __name__ == '__name__':
    startUtility()