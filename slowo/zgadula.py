import numpy
import dict1
import dict2
import pandas
import re
import difflib

class Guesser:
    def __init__(self, dictionary: int, encodedWord: str) -> None:
        if dictionary == 1:
            self.wordlist = numpy.sort(numpy.array(dict1.dict1[encodedWord]))
        elif dictionary == 2:
            self.wordlist = numpy.sort(numpy.array(dict2.dict2[encodedWord]))
        self.usedLetters = []
        self.dict = dictionary
        self.encodedWord = encodedWord

    def countLetters(self): # counts letter ocurrences in candidate words
        return pandas.Series(list(''.join(self.wordlist))).value_counts().to_dict()

    def pickLetter(self): # picks most common letter to guess
        letters = list(self.countLetters().keys())
        for i in range(len(letters)):
            if letters[i] not in self.usedLetters:
                self.usedLetters.append(letters[i])
                print(f"Picked letter {letters[i]}")
                return letters[i]

    def updateCandidates(self, guessedLetter, positions): # when letter guessed
        #print(positions)
        pattern = re.compile(str(positions).replace('1', guessedLetter).replace('0', f'[^{guessedLetter}]'))
        #print(pattern)
        self.wordlist = numpy.sort(numpy.array(list(filter(pattern.match, self.wordlist))))


    def rejectCandidates(self, letter): # when letter not guessed
        for word in self.wordlist:
            if letter in word:
                self.wordlist = numpy.sort(numpy.delete(self.wordlist, numpy.argwhere(self.wordlist == word)))

    def findDifferences(self): # when not many candidates
        for i in range(len(self.wordlist)):
            for position, letter  in enumerate(difflib.ndiff(self.wordlist[i], self.wordlist[i+1])):
                if letter[0] == " ": 
                    continue
                else:
                    if letter[-1] not in self.usedLetters:
                        self.usedLetters.append(letter[-1])
                        print(f"Picked letter {letter[-1]}")
                        return letter[-1]
                    else:
                        continue
    
    def move(self):
        print(f"Possible words: {self.wordlist}")
        print(f"Words left: {len(self.wordlist)}")
        if len(self.wordlist) == 2 or len(self.wordlist) == 1:
            word = self.wordlist[0]
            print(f"Trying word {word}")
            self.wordlist = numpy.delete(self.wordlist, numpy.argwhere(self.wordlist == word))
            return "=\n" + word
        elif len(self.wordlist) <= 15 and len(self.wordlist) > 2:
            return "+\n" + self.findDifferences()
        elif len(self.wordlist) == 0:
            return ""
        else:
            return "+\n" + self.pickLetter()
