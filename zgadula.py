import numpy
import dict1
import dict2
from collections import Counter
import pandas
import re

def countLetters(wordlist):
    return pandas.Series(list(''.join(wordlist))).value_counts().to_dict()

def pickLetter(wordlist):
    return list(countLetters(wordlist).keys())[0]

def findCandidates(dict, encodedWord):
    return numpy.array(dict[encodedWord])

def rejectCandidates(wordlist, guessedLetter, positions):
    pattern = re.compile(str(positions).replace('1', guessedLetter).replace('0', '.'))
    matching = list(filter(pattern.match, wordlist))
    return numpy.array(matching)

if __name__ == '__main__':
    #print(countLetters()
    print(rejectCandidates(findCandidates(dict1.dict1, '111'), 'a', '100'))
    # print(pickLetter(dict1.dict1['11']))
    # print()