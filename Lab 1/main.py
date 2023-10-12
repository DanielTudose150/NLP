# https://www.nltk.org/howto/wordnet.html
# https://github.com/svisser/crossword

from types import NoneType
import nltk
from nltk.corpus import wordnet as wn
import random

# Create a crossword puzzle game with at least 7 words from a specific
# user suggested theme. Use wordnet and nltk to automatically generate clues
# which should be a combo of definitions, synonyms, antonyms or other wn relations

# 1. verificam daca sunt 7 cuvinte potentiale in hyper/hyponyms
# 2. daca nu, cautam in synonyms etc
# 3. pentru fiecare cuvant dam o definitie/altele si asteptam inputul userului

tematica = input("Enter a Theme (one word only): ")

syns = wn.synsets(tematica)[0]
print(syns.definition())

words = []
# print(syns.hypernyms())
# print(syns.hyponyms())

if len(syns.hyponyms()) >= 7:
    for i in range(0, 7):
        hyponym = syns.hyponyms()[i]
        words.append(hyponym.lemma_names('eng')[0])
# the else case where we go to synonyms
else:
    for i in range(0, len(syns.hyponyms())):
        # i1 = random.randint(0,len(syns.hyponyms()))
        words.append(syns.hyponyms()[i].lemma_names('eng')[0])
    if len(wn.synonyms(tematica)) != 0:
        i1 = 0
        for i in range(len(syns.hyponyms()), 7):
            words.append(wn.synonyms(tematica)[i1])
            i1 = i1 + 1

print(words)
print('-------------------')
print(syns.lemma_names('eng'))

# check if it's an adjective. if so, antomyms and synonyms are clear
# if(len(wn.synsets(tematica, wn.ADJ)) !=0):
#     #print(syns.antonyms())
#     print(syns.lemmas()[0].antonyms())
#     print(syns.lemmas()[0].synonyms())

# print(syns.hyponyms()[3].definition())
# print(syns.hyponyms()[3].lemma_names('eng'))
# print('-------------------')

# hypon = wn.morphy(syns.hyponyms()[3].lemma_names[0], wn.NOUN)
# print(hypon)

def definitia(cuvant):
    syns = wn.synsets(cuvant)[0]
    definition = syns.definition()
    if (cuvant in definition):
        stg = definition.find(cuvant)
        definition2 = definition[0:stg - 1] + definition[stg + len(cuvant):]
        #print(definition2)
        return (definition2)
    else:
        if (len(definition) == 0):
            # print("No definition available")
            return "-"

    return definition


def exemplul(cuvant):
    syns =  wn.synsets(cuvant)[0]
    if (len(syns.examples())) != 0:
        example = syns.examples()[0]
        if (cuvant in example):
            stg = example.find(cuvant)
            if stg >= 0:
                example2 = example[0:stg - 1] + ' '
                for i in range(0, len(cuvant)):
                    example2 = example2 + '_'
                example2 = example2 + ' ' + example[stg + len(cuvant):]
                #print(example2)
                return example2
    print('No example available')
    return " "


def hyponymul(cuvant):
    if (len(syns.hyponyms())) != 0:
        hyponym = syns.hyponyms()[0]
        # print(hyponym.lemma_names('eng')[0])
        return hyponym.lemma_names('eng')[0]
    else:
        # print('No hyponym available')
        return " "


def hypernymul(cuvant):
    if (len(syns.hypernyms())) != 0:
        hypernym = syns.hypernyms()[0]
        # print(hypernym.lemma_names('eng')[0])
        return hypernym.lemma_names('eng')[0]
    else:
        ##print('No hypernym available')
        return " "


def synonymul(cuvant):
    if len(wn.synonyms(cuvant)) != 0:
        # #choose a random synonym from the list of lists
        # i1 = random.randint(0, len(wn.synonyms(cuvant)) - 1)
        # i2 = random.randint(0, len(wn.synonyms(cuvant)[i1]) - 1)
        # #print(wn.synonyms(cuvant)[i1][i2])
        # return wn.synonyms(cuvant)[i1][i2]
        if wn.synonyms(cuvant):
            i1 = random.randint(0, len(wn.synonyms(cuvant)) - 1)
            synonym_set = wn.synonyms(cuvant)[i1]
            if synonym_set:
                i2 = random.randint(0, len(synonym_set) - 1)
                return synonym_set[i2]
    else:
        # print('A synonym cannot be found')
        return "-"


def antonymul(cuvant):
    synss = wn.synsets(cuvant)[0]
    synss.lemmas()[0].antonyms()
    if len(synss.lemmas()[0].antonyms()) != 0:
        # print(synss.lemmas()[0].antonyms())
        return synss.lemmas()[0].antonyms()
    else:
        # print('An antonym cannot be found')
        return " "

def printGrid(grid, h):
    for i in range(h):
        print(grid[i])


def createGrid(words):
    info = {}
    for word in words:
        info[word] = {
            "length": len(word),
            "start": {
                "row": 0,
                "col": 0
            },
            "end": {
                "row": 0,
                "col": 0
            },
            "dir": -1
        }

    sortedWords = sorted(words, key=lambda x: info[x]["length"], reverse=True)
    grid = [["+" for _ in range(100)] for _ in range(100)]
    addedOrder = []

    i = 0
    # placing 1st word in the middle of the matrix
    for j in range(50 - len(sortedWords[0]) // 2, 100):
        if i == 0:
            info[sortedWords[0]]["start"] = {"row": 50, "col": j}
            info[sortedWords[0]]["dir"] = 1
        if i == len(sortedWords[0]):
            info[sortedWords[0]]["end"] = {"row": 50, "col": j - 1}
            break

        grid[50][j] = sortedWords[0][i]
        i += 1
    addedOrder.append(sortedWords[0])
    # placing the other words inside
    for i in range(1, len(sortedWords)):
        placeable = False

        curr = sortedWords[i]
        # print("Trying to add ", curr)
        # check if they have common character with other placed  words
        commons = []
        for l, w in enumerate(addedOrder):
            commonC = []
            for k, c in enumerate(curr):
                if c in w:
                    commonC.append((c, k, w.find(c)))
            commons.append((l, commonC))

        # check if placeable
        for el in commons:
            if placeable:
                break
            if info[addedOrder[el[0]]]["dir"] == 1:
                for pair in el[1]:
                    plOk = True
                    for cn, row in enumerate(range(info[addedOrder[el[0]]]["start"]["row"] - pair[1],
                                                   info[addedOrder[el[0]]]["start"]["row"] - pair[1] + info[curr][
                                                       "length"])):
                        if grid[row][info[addedOrder[el[0]]]["start"]["col"] + pair[2]] != "+":
                            if cn == pair[1]:
                                continue
                            plOk = False
                            break
                    if plOk:
                        # place word in grid
                        for cn, row in enumerate(range(info[addedOrder[el[0]]]["start"]["row"] - pair[1],
                                                       info[addedOrder[el[0]]]["start"]["row"] - pair[1] + info[curr][
                                                           "length"])):
                            grid[row][info[addedOrder[el[0]]]["start"]["col"] + pair[2]] = curr[cn]
                        addedOrder.append(curr)
                        info[curr]["start"] = {"row": info[addedOrder[el[0]]]["start"]["row"] - pair[1],
                                               "col": info[addedOrder[el[0]]]["start"]["col"] + pair[2]}
                        info[curr]["end"] = {
                            "row": info[addedOrder[el[0]]]["start"]["row"] - pair[1] + info[curr]["length"],
                            "col": info[addedOrder[el[0]]]["start"]["col"] + pair[2]}
                        info[curr]["dir"] = 3 - info[addedOrder[el[0]]]["dir"]
                        placeable = True
                        # print("Added ", curr, " to ", addedOrder[el[0]], " ", el[0])
                        break
            elif info[addedOrder[el[0]]]["dir"] == 2:
                for pair in el[1]:
                    plOk = True
                    for rn, col in enumerate(range(info[addedOrder[el[0]]]["start"]["col"] - pair[1],
                                                   info[addedOrder[el[0]]]["start"]["col"] - pair[1] + info[curr][
                                                       "length"])):
                        if grid[info[addedOrder[el[0]]]["start"]["row"] + pair[2]][col] != "+":
                            if rn == pair[1]:
                                continue
                            plOk = False
                            break
                    if plOk:
                        # place word in grid
                        for rn, col in enumerate(range(info[addedOrder[el[0]]]["start"]["col"] - pair[1],
                                                       info[addedOrder[el[0]]]["start"]["col"] - pair[1] + info[curr][
                                                           "length"])):
                            grid[info[addedOrder[el[0]]]["start"]["row"] + pair[2]][col] = curr[rn]

                        addedOrder.append(curr)
                        info[curr]["start"] = {"row": info[addedOrder[el[0]]]["start"]["row"] + pair[2],
                                               "col": info[addedOrder[el[0]]]["start"]["col"] - pair[1]}
                        info[curr]["end"] = {"row": info[addedOrder[el[0]]]["start"]["row"] + pair[2],
                                             "col": info[addedOrder[el[0]]]["start"]["col"] - pair[1] + info[curr][
                                                 "length"]}
                        info[curr]["dir"] = 3 - info[addedOrder[el[0]]]["dir"]
                        placeable = True
                        # print("Added ", curr, " to ", addedOrder[el[0]], " ", el[0])
                        break
        if placeable:
            pass
        else:
            highestRow = 0
            highestCol = 0
            for w in addedOrder:
                if info[w]["dir"] == 2:
                    if info[w]["end"]["row"] > highestRow:
                        highestRow = info[w]["end"]["row"] + 1
                        highestCol = addedOrder[0]["start"]["col"]
            for col, c in enumerate(curr):
                grid[highestRow][col] = c

            addedOrder.append(curr)
            info[curr]["start"] = {"row": highestRow, "col": highestCol}
            info[curr]["end"] = {"row": highestRow, "col": highestCol + info[curr]["length"]}
            info[curr]["dir"] = 1
            # print("Added ", curr, " outside of crossword puzzle.")

    # printGrid(grid, 100)

    # trim grid
    lowestRow = 100
    leftestCol = 100
    highestRow = 0
    rightestCol = 0

    for w in addedOrder:
        if info[w]["start"]["row"] < lowestRow:
            lowestRow = info[w]["start"]["row"]
        if info[w]["start"]["col"] < leftestCol:
            leftestCol = info[w]["start"]["col"]
        if info[w]["end"]["row"] > highestRow:
            highestRow = info[w]["end"]["row"]
        if info[w]["end"]["col"] > rightestCol:
            rightestCol = info[w]["end"]["col"]

    maxi = 0
    for w in addedOrder:
        info[w]["start"]["row"] -= (lowestRow)
        info[w]["start"]["col"] -= (leftestCol )
        if info[w]["dir"] == 1:
            info[w]["end"]["row"] = info[w]["start"]["row"]
            info[w]["end"]["col"] = info[w]["start"]["col"] + info[w]["length"]
            if info[w]["end"]["col"] > maxi:
                maxi = info[w]["end"]["col"]
        elif info[w]["dir"] == 2:
            info[w]["end"]["col"] = info[w]["start"]["col"]
            info[w]["end"]["row"] = info[w]["start"]["row"] + info[w]["length"]
            if info[w]["end"]["row"] > maxi:
                maxi = info[w]["end"]["row"]

    grid = [[" " for _ in range(maxi + 1)] for _ in range(maxi + 1)]

    for w in addedOrder:
        if info[w]["dir"] == 1:
            for j, c in enumerate(range(info[w]["start"]["col"], info[w]["end"]["col"])):
                grid[info[w]["start"]["row"]][c] = "@"
        elif info[w]["dir"] == 2:
            for i, r in enumerate(range(info[w]["start"]["row"], info[w]["end"]["row"])):
                grid[r][info[w]["start"]["col"]] = "@"

    printGrid(grid, maxi + 1)

    return info, grid, maxi

def printGrid2(info, grid, h, w):
    if info[w]["dir"] == 1:
        for j, c in enumerate(range(info[w]["start"]["col"], info[w]["end"]["col"])):
            grid[info[w]["start"]["row"]][c] = w[j]
    elif info[w]["dir"] == 2:
        for i, r in enumerate(range(info[w]["start"]["row"], info[w]["end"]["row"])):
            grid[r][info[w]["start"]["col"]] = w[i]

    printGrid(grid, h)

def wordsAndClues(words):
    for word in words:
        ok = random.randint(0, 100) % 3
        exem = exemplul(word)
        defi = definitia(word)
        sino = synonymul(word)
        if (ok == 0 and exem == " "):
            ok = 1
        else:
            if ok == 2 and sino == "-":
                if exem == " ":
                    ok = 1
                else:
                    ok = 0
        if ok == 0:
            clue = exemplul(word)
            print("The clue for this word is: " + clue)
            raspunsUser = input("Your answer: ")
            while word != raspunsUser:
                raspunsUser = input("Try again. Your new answer: ")

        else:
            if ok == 1:
                clue = definitia(word)
                print("The clue for this word is: " + clue)
                raspunsUser = input("Your answer: ")
                while word != raspunsUser:
                    raspunsUser = input("Try again. Your new answer: ")

            else:
                if synonymul(word) != "-" and type(synonymul(word)) != NoneType:
                    clue = synonymul(word)
                    print("The clue for this word is: " + clue)
                    raspunsUser = input("Your answer: ")
                    while word != raspunsUser:
                        raspunsUser = input("Try again. Your new answer: ")

                else:
                    clue = definitia(word)
                    print("The clue for this word is: " + clue)
                    raspunsUser = input("Your answer: ")
                    while word != raspunsUser:
                        raspunsUser = input("Try again. Your new answer: ")
        print("Great answer! Have a look at the crossword puzzle now and let's move on!")
        printGrid2(gInfo, gGrid, gMaxi, word)

gInfo, gGrid, gMaxi = createGrid(words)
print("---------------------------------")

wordsAndClues(words)
