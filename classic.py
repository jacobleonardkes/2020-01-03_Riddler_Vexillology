import requests # need to pip3 install requests

r = requests.get('https://norvig.com/ngrams/enable1.txt')
words = r.text.split('\n')

def orderedLetters(word):
    letters = list(set(word))
    letters.sort()
    return ''.join(letters)

validWords = list(filter(lambda x: len(x) >= 4 and 's' not in x and len(orderedLetters(x)) <= 7, words))

orderMap = dict()
for word in validWords:
    letters = orderedLetters(word)
    score = len(word)
    if len(letters) == 7:
        score += 7
    orderMap[letters] = orderMap.get(letters, []) + [(word, score)]

print('Found %d valid words out of %d total words with %d unique letter sets' % (len(validWords), len(words), len(orderMap)))

validPangrams = list(filter(lambda x: len(orderedLetters(x)) == 7, validWords))
print('Found %d valid pangrams from %s to %s' % (len(validPangrams), validPangrams[0], validPangrams[-1]))
validLetterSets = set(map(orderedLetters, validPangrams))
validBoards = set()
for validLetterSet in validLetterSets:
    for letter in validLetterSet:
        validBoards.add((letter, validLetterSet.replace(letter,'')))
print('Found %d valid boards' % len(validBoards))

bestBoard = None
bestScore = 0
bestWords = []
for center,nonCenterLetters in validBoards:
    thisScore = 0
    theseWords = []
    boardSet = set(list(nonCenterLetters) + [center])
    for letters, wordScores in orderMap.items():
        if center in letters and boardSet.issuperset(set(letters)):
            for word, score in wordScores:
                thisScore += score
                theseWords.append('%s(%d)' % (word, score))
    if thisScore > bestScore:
        bestScore = thisScore
        bestBoard = (center, nonCenterLetters)
        bestWords = theseWords
        print('Center: %s, Others: %s, Score: %d, Words: %s' % (center, nonCenterLetters, bestScore, ', '.join(bestWords)))
