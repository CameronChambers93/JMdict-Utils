from JMdictToJSON import JMdictToJSON
from RandomWordsToJSON import RandomWordsToJSON
from QuerySpeedtest import QuerySpeedtest
from GenerateJLPTLists import GenerateJLPTLists

if __name__ == '__main__':
    try:
        JMdictToJSON.start(0, False)
        RandomWordsToJSON.startUtility(min_word_length=4)
        QuerySpeedtest.startUtility()
        GenerateJLPTLists.startUtility()
        print('\All tests passed!\n')
    except:
        print('\nTests failed, please see output for more details...\n')