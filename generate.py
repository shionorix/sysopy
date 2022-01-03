import numpy

def transcript_word(word, dict):
    letter_values1 = {
        'w':1, 'e':1, 'r':1, 'u':1, 'i':1,'o':1, 'a':1, 's':1, 'z':1, 'x':1, 'c':1, 'v':1, 'n':1, 'm':1, 'ę':1, 'ó':1, 'ą':1, 'ś':1, 'ń':1, 'ć':1, 'ż':1, 'ź':1,
        'p':2, 'y':2, 'j':2, 'g':2, 'q':2,
        't':3, 'l':2, 'b':2, 'd':2, 'h':2, 'k':2, 'ł': 2,
        'f':4
            }
    letter_values2 = {
        'a':1, 'c':1, 'e':1, 'm':1, 'n':1, 'o':1, 'r':1, 's':1, 'u':1, 'w':1, 'z':1, 'x':1, 'v':1,
        'ą':2, 'ę':2, 'g':2, 'j':2, 'p':2, 'y':2, 'q':2,
        'b':3, 'ć':3, 'd':3, 'h':3, 'k':3, 'l':3, 'ł':3, 'ń':3, 'ó':3, 'ś':3, 't':3, 'ź':3, 'ż':3, 'i':3,
        'f':4
    }
    coded_word = ''
    if dict == 1:
        for i in range(len(word)):
            coded_word += str(letter_values1[word[i]])
        return coded_word
    elif dict == 2:
        for i in range(len(word)):
            coded_word += str(letter_values2[word[i]])
        return coded_word

dict = {}
with open('slowa.txt', 'r', encoding="UTF-8") as slowa:
    for line in slowa:
        coded_word = transcript_word(line.rstrip('\n'), 1)
        if coded_word in dict:
            dict[coded_word].append(line.rstrip('\n'))
        else:
            dict[coded_word] = [line.rstrip('\n')]

dictionary = open("dict1.py", "w", encoding="UTF-8")
dictionary.write(f"dict1 = {dict}")
