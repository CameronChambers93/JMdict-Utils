# Original attempt at parsing JMdict, kept for posterity.

# I found out afterwards that parsing XML manually is time-consuming and dangerous

# I also over-engineered this process with the inclusion of classes. I wanted to gain some
# more experience working with classes in python, but am avoiding it in future iterations


from copy import Error
import sys
import pdb
import os
import re
import time
import math
import JMdictUtils
from tqdm import tqdm

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = os.path.abspath(os.path.join(__file__, '../../Resources/'))
FILENAME = os.path.join(RESOURCE_DIR, 'JMdict_e')

OUTPUT_FILENAME = os.path.join(RESOURCE_DIR, "JMdict_e.json")


# Class used to handle spacing and newlines when printing text
class Text:
    def getWhitespace(self, indent, initialIndent) -> str:
        return ' '*(indent + initialIndent)

    def getNewline(self, indent) -> str:
        return '' if indent == 0 else '\n'

    def getSpace(self, indent) -> str:
        return '' if indent == 0 else ' '

# Class for entries of the JMDict. Each has the following form:
#
# ent_seq: int
# k_ele: k_ele*
# r_ele: r_ele*
# sense: sense+
class Entry(Text):
    def __init__(self, ent_seq, k_ele, r_ele, sense):
        self.ent_seq = ent_seq
        self.k_ele = k_ele
        self.r_ele = r_ele
        self.sense = sense

    def getEnt_seqString(self, indent=0, initalIndent=0):
        return self.ent_seq.toString(indent, initalIndent)

    def getFieldString(self, name, ele, indent=0, initialIndent=0):
        if len(ele) == 0: return ''
        whitespace1 = self.getWhitespace(indent, initialIndent)
        whitespace2 = self.getWhitespace(indent, initialIndent + indent)
        newline = self.getNewline(indent)
        space = self.getSpace(indent)
        msg = ',{newline}{whitespace1}"{name}":{space}['.format(name=name, newline=newline, whitespace1=whitespace1, space=space)
        for i in range(len(ele)):
            e = ele[i]
            comma = ',' if i > 0 else ''
            value = e.toString(indent, initialIndent + indent*2)
            msg += '{comma}{newline}{whitespace2}{value}'.format(comma=comma, newline=newline, whitespace2=whitespace2, value=value)
        msg += '{newline}{whitespace1}]'.format(newline=newline, whitespace1=whitespace1)
        return msg

    def toString(self, indent=0, initialIndent=0, comma=',') -> str:
        msg = ""
        ent_seq = self.getEnt_seqString(indent, initialIndent)
        k_ele = self.getFieldString('k_ele', self.k_ele, indent, initialIndent)
        r_ele = self.getFieldString('r_ele', self.r_ele, indent, initialIndent)
        sense = self.getFieldString('sense', self.sense, indent, initialIndent)
        newline = self.getNewline(indent)
        whitespace = self.getWhitespace(indent, initialIndent-indent)
        msg = '{{{ent_seq}{k_ele}{r_ele}{sense}{newline}{whitespace}}}{comma}'.format(ent_seq=ent_seq, k_ele=k_ele, r_ele=r_ele, sense=sense, newline=newline, whitespace=whitespace, comma=comma)
        return msg

# Contains information about the entry, including definitions, origins, synonyms, antonyms, etc.
# All fields have the following form:
#
# field: [string]*
class Sense(Text):
    def __init__(self, stagk, stagr, pos, xref, ant, field, misc, s_inf, lsource, dial, gloss):
        self.fields = {}
        if (not len(stagk) == 0):
            self.fields['stagk'] = Stagk(stagk) 
        if (not len(stagr) == 0):
            self.fields['stagr'] = Stagr(stagr)
        if (not len(pos) == 0):
            self.fields['pos'] = Pos(pos)
        if (not len(xref) == 0):
            self.fields['xref'] = Xref(xref)
        if (not len(ant) == 0):
            self.fields['ant'] = Ant(ant)
        if (not len(field) == 0):
            self.fields['field'] = Field(field)
        if (not len(misc) == 0):
            self.fields['misc'] = Misc(misc)
        if (not len(s_inf) == 0):
            self.fields['s_inf'] = S_inf(s_inf)
        if (not len(lsource) == 0):
            self.fields['lsource'] = Lsource(lsource)
        if (not len(dial) == 0):
            self.fields['dial'] = Dial(dial)
        if (not len(gloss) == 0):
            self.fields['gloss'] = Gloss(gloss)

    def toString(self, indent=0, initialIndent=0):
        newline = self.getNewline(indent)
        whitespace1 = self.getWhitespace(indent, initialIndent-indent)
        msg = '{'
        addComma = False
        for item in self.fields.items():
            comma = ',' if addComma else ''
            addComma = True
            value = item[1].toString(indent, initialIndent)
            msg += '{comma}{value}'.format(comma=comma, value=value)
        msg += '{newline}{whitespace1}}}'.format(newline=newline, whitespace1=whitespace1)
        return msg

# Contains information about kanji in an entry (if kanji exists)
# Has the following form:
#
# keb: int
# ke_inf: [string]*
# ke_pri: [string]*
class K_Ele(Text):
    def __init__(self, keb, ke_inf, ke_pri):
        self.keb = keb
        self.ke_inf = Ke_inf(ke_inf)
        self.ke_pri = Ke_pri(ke_pri)

    def toString(self, indent=0, initialIndent=0):
        keb = self.keb.toString(indent, initialIndent, '')
        ke_inf = self.ke_inf.toString(indent, initialIndent, ',')
        ke_pri = self.ke_pri.toString(indent, initialIndent, ',')
        newline = self.getNewline(indent)
        whitespace = self.getWhitespace(indent, initialIndent - indent)
        msg = '{{{keb}{ke_inf}{ke_pri}{newline}{whitespace}}}'.format(keb = keb, ke_inf = ke_inf, ke_pri = ke_pri, newline=newline, whitespace=whitespace)
        return msg

# Contains information about the reading of an entry
# Has the following form:
#
# keb: int
# ke_inf: [string]*
# ke_pri: [string]*
class R_Ele(Text):
    def __init__(self, reb, re_nokanji, re_restr, re_inf, re_pri):
        self.reb = reb
        self.re_nokanji = Re_nokanji(re_nokanji)
        self.re_restr = Re_restr(re_restr)
        self.re_inf = Re_inf(re_inf)
        self.re_pri = Re_pri(re_pri)

    def toString(self, indent=0, initialIndent=0):
        reb = self.reb.toString(indent, initialIndent, '')
        re_nokanji = self.re_nokanji.toString(indent, initialIndent, ',')
        re_restr = self.re_restr.toString(indent, initialIndent, ',')
        re_inf = self.re_inf.toString(indent, initialIndent, ',')
        re_pri = self.re_pri.toString(indent, initialIndent, ',')
        newline = self.getNewline(indent)
        whitespace = self.getWhitespace(indent, initialIndent - indent)
        msg = '{{{reb}{re_nokanji}{re_restr}{re_inf}{re_pri}{newline}{whitespace}}}'.format(reb=reb, re_nokanji=re_nokanji, re_restr = re_restr, re_inf=re_inf, re_pri=re_pri, newline=newline, whitespace=whitespace)
        return msg

# Will be used to process tags and connections between words
class Entities:
    def __init__(self):
        self.entities = {}

    def addEntityType(self, entityType, entityName):
        self.entities[entityType] = {'__name__': entityName}

    def addEntity(self, entityType, entityName, entityValue):
        self.entities[entityType][entityName] = entityValue

# Used for elements with a single value
class PCData(Text):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def toString(self, indent=0, initialIndent=0, comma=''):
        value= self.getValue()
        if type(value) == bool:
            if value == False:
                return ''
            else:
                value = 'true'  # Undo Python's boolean capitalization
        elif value == None or len(value) == 0:
            return ''
        newline = self.getNewline(indent)
        whitespace = self.getWhitespace(indent, initialIndent)
        name = self.getName()
        space = self.getSpace(indent)
        msg = '{comma}{newline}{indent}"{name}":{space}"{value}"'.format(comma=comma, indent=whitespace, name=name, value=value, space=space, newline=newline)
        return msg

    def getValue(self):
        if type(self.value) == str:
            return self.value.replace('"', '\\"')   # Make sure double quotes are escaped properly
        else:
            return self.value

    def getName(self):
        return self.name

# Used for elements with multiple values
class PCDataArray(PCData):
    def __init__(self, name, values):
        pcdata = []
        for value in values:
            pcdata.append(value)
        super().__init__(name, pcdata)

    def toString(self, indent=0, initialIndent=0, comma=''):
        values = self.getValue()
        if len(values) == 0: return ''
        newline = self.getNewline(indent)
        whitespace1 = self.getWhitespace(indent, initialIndent)
        whitespace2 = self.getWhitespace(indent*2, initialIndent)
        space = self.getSpace(indent)
        name = self.getName()
        msg = '{comma}{newline}{indent1}"{name}":{space}['.format(comma=comma, newline=newline, indent1=whitespace1, name=name, space=space)
        for i in range(len(values)):
            value = values[i].getValue()
            msg += '{newline}{whitespace2}"{value}"'.format(newline = newline, whitespace2 = whitespace2, value=value)
            msg += ',' if i < len(values) - 1 else ''
        msg += "{newline}{indent1}]".format(newline=newline, indent1=whitespace1)
        return msg

# Id for a given entry
class Ent_seq(PCData):
    def __init__(self, value):
        super().__init__('ent_seq', value)

# The writing of the element, if it contains kanji characters
class Keb(PCData):
    def __init__(self, value):
        super().__init__('keb', value)

# Field related to the orthography of the element
class Ke_inf(PCDataArray):
    def __init__(self, value):
        super().__init__('ke_inf', value)

# Along with re_pri, will contain information about the 'relative priority of a word'
# For instance, if the tag 'news1/news2' is present, that indicates the word is used often in news publications,
#   and as such can be considered a 'highly used' word
class Ke_pri(PCDataArray):
    def __init__(self, value):
        super().__init__('ke_pri', value)

# The reading of the element
class Reb(PCData):
    def __init__(self, value):
        super().__init__('reb', value)

# Indicates that the reb, while associated with the keb of an element, cannot be regarded as a true reading of the kanji
class Re_nokanji(PCData):
    def __init__(self, value):
        super().__init__('re_nokanji', value)

    def toString(self, indent, initialIndent, comma):
        if self.getValue():
            return super(Re_nokanji, self).toString(indent, initialIndent, comma)
        else:
            return ''
        
# Used to indicate that the reading only applies to a subset of the keb elements in the entry
class Re_restr(PCDataArray):
    def __init__(self, value):
        super().__init__('re_restr', value)

# Information pertaining to the specific reading. Typically will be used to indicate some unusual aspect of the reading
class Re_inf(PCDataArray):
    def __init__(self, value):
        super().__init__('re_inf', value)

# See Ke_pri
class Re_pri(PCDataArray):
    def __init__(self, value):
        super().__init__('re_pri', value)

#
class Stagk(PCDataArray):
    def __init__(self, value):
        super().__init__('stagk', value)

# If present, indicate that the sense is restricted to the lexeme represented by the keb and/or the reb
class Stagr(PCDataArray):
    def __init__(self, value):
        super().__init__('stagr', value)

# Part of speech information about the entry. 
# In general where there are multiple senses in an entry, the part-of-speech of an earlier sense will apply to
#     later senses unless there is a new part-of-speech indicated.
class Pos(PCDataArray):
    def __init__(self, value):
        super().__init__('pos', value)

# Used to indicate a cross-reference to another entry with a similar or related meaning or sense
class Xref(PCDataArray):
    def __init__(self, value):
        super().__init__('xref', value)

# Used to indicate another entry which is an antonym of the current entry/sense. The content of this element must exactly
#     match that of a keb or reb element in another entry.
class Ant(PCDataArray):
    def __init__(self, value):
        super().__init__('ant', value)

# Information about the field of application of the entry/sense (computers, economics, music, etc.)
class Field(PCDataArray):
    def __init__(self, value):
        super().__init__('field', value)

# This element is used for other relevant information about the entry/sense. As with part-of-speech, 
#     information will usually apply to several senses.
class Misc(PCDataArray):
    def __init__(self, value):
        super().__init__('misc', value)

# The sense-information elements provided for additional information to be recorded about a sense. Typical usage would
#     be to indicate such things as level of currency of a sense, the regional variations, etc.
class S_inf(PCDataArray):
    def __init__(self, value):
        super().__init__('s_inf', value)

# This element records the information about the source language(s) of a loan-word/gairaigo.
# If the source language is other than English, the language is indicated by the xml:lang attribute
class Lsource(PCDataArray):
    def __init__(self, value):
        super().__init__('lsource', value)

# For words specifically associated with regional dialects in Japanese, the entity code for that dialect, e.g. ksb for Kansaiben.
class Dial(PCDataArray):
    def __init__(self, value):
        super().__init__('dial', value)

# Target-language words or phrases which are equivalents to the Japanese word defined in an entry.
# This element would normally be present, however it may be omitted in entries which are purely for a cross-reference.
class Gloss(PCDataArray):
    def __init__(self, value):
        super().__init__('gloss', value)

class Controller(Text):
    def __init__(self):
        self.entities = Entities()
        self.entries = {}

    def addEntityType(self, line) -> str:
        line = re.sub(r'[<>]', '', line)
        words = line.split(' ')
        entityType = words[0]
        entityName = words[1] if len(words) > 2 else words[0]
        self.entities.addEntityType(entityType, entityName)
        return entityType
        
    def processEntities(self, line):
        line = re.sub(r'<!-- | -->\n', '', line)
        if '<' in line:
            entityType = self.addEntityType(line)
            line = self.getNextLine()
            while ('<!--' not in line):
                line = re.sub(r'<!ENTITY |>', '', line)
                words = line.split(' ', maxsplit=1)
                entityName = words[0]
                entityValue = words[1]
                self.entities.addEntity(entityType, entityName, entityValue)
                line = self.getNextLine()
                
    def parseEnt_seq(self, line) -> str:
        return Ent_seq(re.sub(r'<[/]*ent_seq>(\n)*', '', line))

    def parseKeb(self, line) -> str:
        return PCData('keb', re.sub(r'<[/]*keb>(\n)*', '', line))

    def parseKe_inf(self, line) -> str:
        return PCData('ke_inf', re.sub(r'<[/]*ke_inf>(\n)*|&|;', '', line))

    def parseKe_pri(self, line) -> str:
        return PCData('ke_pri', re.sub(r'<[/]*ke_pri>(\n)*', '', line))

    def processK_Ele(self):
        line = self.getNextLine()
        keb = self.parseKeb(line)
        ke_inf = []
        ke_pri = []
        line = self.getNextLine()
        while '</k_ele>' not in line:
            if 'ke_inf' in line:
                ke_inf.append(self.parseKe_inf(line))
            elif 'ke_pri' in line:
                ke_pri.append(self.parseKe_pri(line))
            line = self.getNextLine()
        return K_Ele(keb, ke_inf, ke_pri)



    def parseReb(self, line) -> str:
        return Reb(re.sub(r'<[/]*reb>(\n)*', '', line))
    
    def parseRe_restr(self, line) -> str:
        return PCData('re_restr', re.sub(r'<[/]*re_restr>(\n)*', '', line))
    
    def parseRe_pri(self, line) -> str:
        return PCData('re_pri', re.sub(r'<[/]*re_pri>(\n)*', '', line))
    
    def parseRe_inf(self, line) -> str:
        return PCData('re_inf', re.sub(r'(;)*<[/]*re_inf>(\n)*(&)*', '', line))
    
    def processR_Ele(self):
        line = self.getNextLine()
        reb = self.parseReb(line)
        line = self.getNextLine()
        if 're_nokanji' in line:
            re_nokanji = True
            line = self.getNextLine()
        else:
            re_nokanji = False
        re_restr = []
        re_inf = []
        re_pri = []
        while '</r_ele>' not in line:
            if 're_restr' in line:
                re_restr.append(self.parseRe_restr(line))
            elif 're_inf' in line:
                re_inf.append(self.parseRe_inf(line))
            elif 're_pri' in line:
                re_pri.append(self.parseRe_pri(line))
            line = self.getNextLine()
        return R_Ele(reb, re_nokanji, re_restr, re_inf, re_pri)
            
    
    def parseStagk(self, line) -> str:
        return PCData('stagk', re.sub(r'<[/]*stagk>(\n)*', '', line))
    
    def parseStagr(self, line) -> str:
        return PCData('stagr', re.sub(r'<[/]*stagr>(\n)*', '', line))
    
    def parsePos(self, line) -> str:
        return PCData('pos', re.sub(r'(;)*<[/]*pos>(\n)*(&)*', '', line))
    
    def parseAnt(self, line) -> str:
        return PCData('ant', re.sub(r'<[/]*ant>(\n)*', '', line))
    
    def parseField(self, line) -> str:
        return PCData('field', re.sub(r'(;)*<[/]*field>(\n)*(&)*', '', line))
    
    def parseMisc(self, line) -> str:
        return PCData('misc', re.sub(r'(;)*<[/]*misc>(\n)*(&)*', '', line))
    
    def parseS_inf(self, line) -> str:
        return PCData('s_inf', re.sub(r'<[/]*s_inf>(\n)*', '', line))
    
    def parseLsource(self, line) -> str:
        if 'xml:lang' in line:
            return PCData('lsource', re.search(r'xml:lang="([a-z]*)"', line).group(1))

    def parseDial(self, line) -> str:
        return PCData('dial', re.sub(r'(;)*<[/]*dial>(\n)*(&)*', '', line))
    
    def parseGloss(self, line) -> str:
        return PCData('gloss', re.sub(r'<[/]*gloss(?:[^>])*>(\n)*', '', line))
    
    def parseXref(self, line) -> str:
        return PCData('xref', re.sub(r'<[/]*xref>(\n)*', '', line))
    
    def processSense(self):
        stagk = []
        stagr = []
        pos = []
        xref = []
        ant = []
        field = []
        misc = []
        s_inf = []
        lsource = []
        dial = []
        gloss = []
        line = self.getNextLine()
        while '</sense>' not in line:
            if '<stagk' in line:
                stagk.append(self.parseStagk(line))
            elif '<stagr' in line:
                stagr.append(self.parseStagr(line))
            elif '<pos' in line:
                pos.append(self.parsePos(line))
            elif '<xref' in line:
                xref.append(self.parseXref(line))
            elif '<ant' in line:
                ant.append(self.parseAnt(line))
            elif '<field' in line:
                field.append(self.parseField(line))
            elif '<misc' in line:
                misc.append(self.parseMisc(line))
            elif '<s_inf' in line:
                s_inf.append(self.parseS_inf(line))
            elif '<lsource' in line and 'xml:lang' in line:
                lsource.append(self.parseLsource(line))
            elif '<dial' in line:
                dial.append(self.parseDial(line))
            elif '<gloss' in line:
                gloss.append(self.parseGloss(line))
            line = self.getNextLine()
        return Sense(stagk, stagr, pos, xref, ant, field, misc, s_inf, lsource, dial, gloss)
    
    def processEntry(self, low_memory=False):
        line = self.getNextLine()
        ent_seq = self.parseEnt_seq(line)
        line = self.getNextLine()
        k_ele = []
        r_ele = []
        sense = []
        while '</entry>' not in line:
            if 'k_ele' in line:
                k_ele.append(self.processK_Ele())
            elif 'r_ele' in line:
                r_ele.append(self.processR_Ele())
            elif 'sense' in line:
                sense.append(self.processSense())
            line = self.getNextLine()
        entry = Entry(ent_seq, k_ele, r_ele, sense)
        if (low_memory):
            return entry
        self.entries[ent_seq.getValue()] = entry

    def getNextLine(self):
        line = self.read_file.readline()
        if line != '':
            self.pbar.update(1)
        return line

    def getLineCount(self):
        return len(open(FILENAME, 'r', encoding='utf8').readlines())

    def loadDict(self, FILENAME):
        self.read_file = open(FILENAME, "r", encoding="utf8")
##          DON'T USE READLINES - No need to load into memory
        line_count = self.getLineCount()
        self.pbar = tqdm(total=line_count)
        line = self.getNextLine()
        while (line != ''):
            if ('<!-- ' in line):
                if ('-->' in line):
                    self.processEntities(line)
                while ('-->' not in line):
                    line = self.getNextLine()
            elif '<entry>' in line:
                self.processEntry()
            try:
                line = self.getNextLine()
            except Exception:
                line = None

    def saveInPlace(self, FILENAME, indent=0, initialIndent=0):
        write_file = open(OUTPUT_FILENAME, "w", encoding="utf8")
        write_file.write("")
        write_file.close()
        newline = self.getNewline(indent)
        whitespace2 = self.getWhitespace(indent, initialIndent-indent)
        msg = self.toStringInPlace(FILENAME, write_file, indent, initialIndent)
        msg = msg[0:-1] # Remove trailing comma
        msg += "{newline}{whitespace2}]".format(newline=newline, whitespace2=whitespace2)
        self.pbar.close()
        self.appendToFile(msg)
        print("\nSuccessfully saved to 'JMdict_e.json")

    def appendToFile(self, msg):
        write_file = open(OUTPUT_FILENAME, "a", encoding="utf8")
        write_file.write(msg)

    def toStringInPlace(self, FILENAME, write_file, indent=0, initialIndent=0):
        msg = "["
        self.count = 0
        self.read_file = open(FILENAME, "r", encoding="utf8")
##          DON'T USE READLINES - No need to load into memory
        line_count = self.getLineCount()
        self.pbar = tqdm(total=line_count)
        line = self.getNextLine()
        while (line != ''):
            if ('<!-- ' in line):
                if ('-->' in line):
                    self.processEntities(line)
                while ('-->' not in line):
                    line = self.getNextLine()
            elif '<entry>' in line:
                msg += self.processEntry(low_memory=True).toString(indent, initialIndent+indent, ',')
                self.count += 1
                if self.count % 10000 == 0:
                    self.appendToFile(msg)
                    msg = ""
            try:
                line = self.getNextLine()
            except Exception:
                line = None
        return msg

    def toString(self, indent=0, initialIndent=0):
        newline = self.getNewline(indent)
        whitespace2 = self.getWhitespace(indent, initialIndent-indent)
        msg = "["
        comma=','
        values = self.entries.values()
        for i in range(len(values)):
            entry = values[i]
            msg += entry.toString(indent, initialIndent+indent, comma)
            if i == len(values) - 1:
                msg = msg[0:-1]
        msg += "{newline}{whitespace2}]".format(newline=newline, whitespace2=whitespace2)
        return msg

    def saveData(self, indent=0, initialIndent=0):
        self.pbar.close()
        print("\nSaving file...")
        with open(OUTPUT_FILENAME, "w", encoding="utf8") as write_file:
            newline = self.getNewline(indent)
            whitespace2 = self.getWhitespace(indent, initialIndent-indent)
            msg = "["
            comma=','
            i = 0
            values = self.entries.values()
            write_file.write(msg)
            for entry in tqdm(values):
                msg = entry.toString(indent, initialIndent+indent, comma)
                if i == len(values) - 1:
                    msg = msg[0:-1]
                i += 1
                write_file.write(msg)
            msg = "{newline}{whitespace2}]".format(newline=newline, whitespace2=whitespace2)
            write_file.write(msg)
            write_file.close()
        print("Successfully saved to {}".format(OUTPUT_FILENAME))

def startController(indent=0, low_memory=False):
    JMdictUtils.checkForDownload()
    controller = Controller()
    print('\nLoading JMdict_e\n')
    epoch = time.time()

    if (low_memory):
        controller.saveInPlace(FILENAME, indent)
    else:
        controller.loadDict(FILENAME)
        controller.saveData(indent)
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
    try:
        indent, low_memory = getArgs()
        startController(indent, low_memory)
    except Exception as e:
        print("Invalid argument '{invalidArg}'".format(invalidArg=e.args[0]))

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
    startController(indent, low_memory)
