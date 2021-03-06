# JMdict-Utils

The purpose of this project was originally just to parse the Japanese-Multilingual Dictionary (JMdict) XML-file in order to produce a usable JSON file for use in other projects. It is growing now to include other functionalities.

All utilities can be accessed by running ```python3 JMdictUtils.py``` or by accessing the scripts directly, as detailed below.

## JMdict
[Information regarding the JMdict project can be found here](https://www.edrdg.org/jmdict/j_jmdict.html)

## JMdictToJSON
### Usage
```
git clone https://github.com/CameronChambers93/JMdict_parser.git
cd JMdict_parser
python3 -m JMDictToJSON.JMDictToJSON [options...]
```
Options
* --indent(-i)=# : Number of leading spaces added to each nested level when outputting JSON
* --low-memory(-m): This mode allows the script to run on machines with low memory. When analytics are added to this project, it is likely that some may not function with this mode enabled

### Output
Current output is hardcoded to fit the needs of my own projects. Revisions will be made to make output format customizable. The following two examples show the format of the output. Note that since certain fields are optional for any given entry, some fields are omitted.


* indent=0
```
{ent_seq:"1004660",k_ele:[{keb:"この外",ke_pri:["spec1"]}],r_ele:[{reb:"このほか",re_pri:["spec1"]}],sense:[{pos:["conj"],misc:["uk"],gloss:["besides","moreover","in addition"]}]}
```
* indent=2
```
{
  ent_seq: "1004660",
  k_ele: [
    {
      keb: "この外",
      ke_pri: [
        "spec1"
      ]
    }
  ],
  r_ele: [
    {
      reb: "このほか",
      re_pri: [
        "spec1"
      ]
    }
  ],
  sense: [
    {
      pos: [
        "conj"
      ],
      misc: [
        "uk"
      ],
      gloss: [
        "besides",
        "moreover",
        "in addition"
      ]
    }
  ]
}
```

## RandomWordsToJSON
### Usage
Outputs a random selection of words to a JSON file for analytical purposes
The script can be ran with the following command:
```
python3 -m RandomWordsToJSON.RandomWordsToJSON [options...]
```

### Options
* --min-word-length(-m)=# : Minimum length for word to lookup. Uses first kanji (hiragana if no kanji exists) of element to get word length

### Output

Currently writes the random words to a JSON file structured the same as the one generated by JMdictToJSON with indent=2

## JMdictToTries
### Usage
Generates two tries from JMdict for word search speed analysis. One trie uses the kanji and hiragana of each entry as 'keys', the other uses the entry sequence.

Currently doesn't output any file/has no usage outside other scripts

## QuerySpeedtest
Uses RandomWords to run lookup queries in order to test retrieval speeds of various methods.

Currently tests against 1) basic Python dictionary and 2) trie data structure
### Usage
```
python3 -m QuerySpeedtest.QuerySpeedtest
```

### Output
Results of the test are written to console

## GenerateJLPTLists
Generates a list of entry ids corresponding to each level of the Japanese Language Proficiency Test (JLPT)
### Usage
```
python3 -m GenerateJLPTLists.GenerateJLPTLists
```

### Output
Outputs a JSON file containing a dictionary. The dictionary has keys 1-5 and the values are arrays containing the ids of every word belonging to that JLPT level.