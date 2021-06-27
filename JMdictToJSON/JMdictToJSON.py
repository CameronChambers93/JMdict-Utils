import os
import re
import time
import JMdictUtils
from tqdm import tqdm
from lxml import etree as ElementTree
import copy
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.abspath(os.path.join(__file__, '../../Resources/'))
FILENAME = os.path.join(RESOURCE_DIR, 'JMdict_e')

OUTPUT_FILENAME = os.path.join(RESOURCE_DIR, "JMdict_e.json")

# Used to correctly track the loading bar. This number refers to the amount of 'inner' XML 
LINE_COUNT_OFFSET = 815622

# I prefer eager initialization of element fields for faster load time - thanks to https://github.com/daffychuy/JMdict_e-Kanjidic-JSON/
# for the inspiration
ENTRY_TEMPLATE = {
    # Don't need to initialize non-array fields
    # "ent_seq": 0,
    "k_ele": [],
    "r_ele": [],
    "sense": []
}

K_ELE_TEMPLATE = {
    # "keb": "",
    "ke_inf": [],
    "ke_pri": []
}

R_ELE_TEMPLATE = {
    # "reb": "",
    # "re_nokanji": False,
    "re_restr": [],
    "re_inf": [],
    "re_pri": []
}

SENSE_TEMPLATE = {
    "stagk": [],
    "stagr": [],
    "pos": [],
    "xref": [],
    "ant": [],
    "field": [],
    "misc": [],
    "s_inf": [],
    "lsource": [],
    "dial": [],
    "gloss": []
}

LSOURCE_TEMPLATE = {
    "lang": "eng",
    # "text": ""
}

def getLineCount():
    return len(open(FILENAME, 'r', encoding='utf8').readlines())

def getModifiedLineCount():
    return len(open(FILENAME, 'r', encoding='utf8').readlines()) - LINE_COUNT_OFFSET

def parseEnt_seq(element, new_ele):
    new_ele['ent_seq'] = element.text

def parseR_ele(elements, new_ele):
    r_ele = copy.deepcopy(R_ELE_TEMPLATE)
    for ele in elements:
        if ele.tag == "reb":
            r_ele['reb'] = ele.text
        elif ele.tag == "re_nokanji":
            r_ele['re_nokanji'] = True
        elif ele.tag == "re_restr":
            r_ele['re_restr'].append(ele.text)
        elif ele.tag == "re_inf":
            r_ele['re_inf'].append(ele.text)
        elif ele.tag == "re_pri":
            r_ele['re_pri'].append(ele.text)
    cleanUpDict(r_ele)
    new_ele['r_ele'].append(r_ele)

def parseK_ele(elements, new_ele):
    k_ele = copy.deepcopy(K_ELE_TEMPLATE)
    for ele in elements:
        if ele.tag == "keb":
            k_ele['keb'] = ele.text
        elif ele.tag == "ke_inf":
            k_ele['ke_inf'].append(ele.text)
        elif ele.tag == "ke_pri":
            k_ele['ke_pri'].append(ele.text)
    cleanUpDict(k_ele)
    new_ele['k_ele'].append(k_ele)

def parseSense(elements, new_ele):
    sense = copy.deepcopy(SENSE_TEMPLATE)
    for ele in elements:
        if ele.tag == "stagk":
            sense['stagk'] = ele.text
        elif ele.tag == "stagr":
            sense['stagr'].append(ele.text)
        elif ele.tag == "pos":
            sense['pos'].append(ele.text)
        elif ele.tag == "xref":
            sense['xref'].append(ele.text)
        elif ele.tag == "ant":
            sense['ant'].append(ele.text)
        elif ele.tag == "field":
            sense['field'].append(ele.text)
        elif ele.tag == "misc":
            sense['misc'].append(ele.text)
        elif ele.tag == "s_inf":
            sense['s_inf'].append(ele.text)
        elif ele.tag == "lsource":
            lsource = copy.deepcopy(LSOURCE_TEMPLATE)
            if ele.values():
                lsource['lang'] = ele.values()[0]
            if ele.text:
                lsource['text'] = ele.text
            sense['lsource'].append(lsource)
        elif ele.tag == "dial":
            sense['dial'].append(ele.text)
        elif ele.tag == "gloss":
            sense['gloss'].append(ele.text)
    cleanUpDict(sense)
    new_ele['sense'].append(sense)

def cleanUpDict(d):
    keys = []
    for key in d.keys():
        keys.append(key)
    for key2 in keys:
        if d[key2] == []:
            d.pop(key2)

def getDictAsStringList():
    lines = []
    with tqdm(total=getLineCount()) as pbar:
        with open(os.path.join(RESOURCE_DIR, 'JMdict_e'), encoding='utf8') as o:
            line = o.readline()
            while line != '':
                lines.append(re.sub('&([A-Za-z0-9-]*);', r"\1", line))
                line = o.readline()
                pbar.update(1)
    return lines

def loadDict():
    f = getDictAsStringList()
    print("\nParsing JMdict...\n")
    parser = ElementTree.XMLParser(resolve_entities=False)
    tree_parser = ElementTree.fromstringlist(f, parser).iter()
    words = []
    for elements in tqdm(tree_parser, total=getModifiedLineCount()):
        if elements.tag == 'entry':
            new_ele = copy.deepcopy(ENTRY_TEMPLATE)
            for ele in elements.iter():
                if ele.tag == "ent_seq":
                    parseEnt_seq(ele, new_ele)
                elif ele.tag == "r_ele":
                    parseR_ele(ele, new_ele)
                elif ele.tag == "k_ele":
                    parseK_ele(ele, new_ele)
                elif ele.tag == "sense":
                    parseSense(ele, new_ele)
            cleanUpDict(new_ele)
            words.append(new_ele)
    return words

def saveData(data, indent=0):
    print("\nSaving file...")
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as write_file:
        if indent:
            json.dump(data, write_file, indent=indent, ensure_ascii=False)
        else:
            json.dump(data, write_file, ensure_ascii=False)
    print("Successfully saved to {}".format(OUTPUT_FILENAME))

def start(indent=0, low_memory=False):
    JMdictUtils.checkForDownload()
    print('\nLoading JMdict_e\n')
    epoch = time.time()

    if (low_memory):
        saveInPlace(indent)
    else:
        words = loadDict()
        saveData(words, indent)
    print('Time elapsed: ' + str(time.time() - epoch))

def getArgs():
    indent, low_memory = 0, False
    args = JMdictUtils.getArgs()
    for arg in args:
        name = arg['name']
        if name == 'low-memory' or name == 'm':
            low_memory = True
            continue
        value = arg['value']
        if name == 'indent' or name == 'i':
            indent = int(value)
        else:
            raise Exception(arg)
    return indent, low_memory
    


if __name__ == '__main__':
    indent = None
    try:
        indent, low_memory = getArgs()
    except Exception as e:
        print("Invalid argument '{invalidArg}'".format(invalidArg=e.args[0]))
    if indent != None:
        start(indent, low_memory)

def getIndentInput():
    try:
        indent = int(input('Indent (default = 0, max 10): '))
        return max(0, min(indent, 10))
    except Exception as e:
        return getIndentInput()
    
def getLowMemoryInput():
    try:
        key = input('Low memory mode (y/n): ')
        if key == 'y':
            return True
        elif key == 'n':
            return False
        else:
            return getIndentInput()
    except Exception as e:
        return getIndentInput()
    

def startUtility():
    print('\n---------- JMdict to JSON ----------\n')
    indent = getIndentInput()
    low_memory = getLowMemoryInput()
    start(indent, low_memory)
