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
python3 JMDictToJSON.py [options]
```
Options
* --indent=number : Number of leading spaces added to each nested level when outputting JSON
* --low-memory: This mode allows the script to run on machines with low memory. When analytics are added to this project, it is likely that some may not function with this mode enabled

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
python3 RandomWordsToJSON.py
```

Options will be available in the future to format the output

### Output
Currently set to output ~10000 words with word length > 6
