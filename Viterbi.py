#Insert Generic comment about system libraries being allowed
import sys
import math

class Viterbi:

    def __init__(self, file):
        self.__file = file
        #Only read the file one time, reference the dictionaries for the rest.
        self.__wordTagCounts, self.__tagCounts, self.__tagForTagCounts, self.__startTagCounts, self.__lineCount = self.__getCounts()
        self.__tagsForWords = self.__getTagsForWords()

    #Calculates the probability a tag starts a sentence,
    #as there's no beginning of sentence tag in the data...
    def __tagStarts(self, tag):
        if self.__lineCount > 0:
            return self.__startTagCounts.get(tag, 0) / self.__lineCount
        return 0

    #Calculates the probability of a tag given a tag.
    def __tagGivenTag(self, tag, prevTag):
        return self.__tagForTagCounts.get(tag+prevTag, 0)/self.__tagCounts.get(prevTag, 0)

    # Calculates the probability of word given a tag
    def __wordGivenTag(self, word, tag):
        if (word+tag) not in self.__wordTagCounts:
            return -math.inf
        return self.__wordTagCounts.get(word+tag, 0)/self.__tagCounts.get(tag, 0)

    #I despise how long this function is, but it's more effort than it's worth to split it up.
    #It also took a long time to get working and I don't want to break it.
    def predict(self, file):
        with open(file, 'r') as data:
            with open("POS.test.out", 'w') as outp:
                for line in data:
                    score = {}
                    backPtr = {}
                    seq = []
                    wordsRaw = line.split()
                    words = []
                    #Cleaning
                    for part in wordsRaw:
                        word = part[0:part.rfind('/')]
                        words.append(word)
                    w = 0
                    for word in words:
                        potTags = self.__tagsForWords.get(word, ["/UKN"])
                        # Initialization
                        score[(potTags[0], w)] = -1
                        backPtr[(potTags[0], w)] = ""
                        if w == 0:
                            for tag in potTags:
                                score[(tag, w)] = self.__wordGivenTag(word, tag) * self.__tagStarts(tag)
                                backPtr[(tag, w)] = 0
                            w = 1
                            continue
                        # Iteration step
                        for tag in potTags:
                            index = (tag, w)
                            #max was reserved :(
                            maxScore = (-math.inf)
                            goodTag = ""
                            prevWord = words[w-1]
                            #Not sure how we were intended to handle cases the prediction word was never observed in training.
                            #My approach is to use an "unknown" tag for these words.
                            prevTags = self.__tagsForWords.get(prevWord, ["/UKN"])
                            for prevTag in prevTags:
                                if prevTag == "/UKN":
                                    goodTag = prevTag
                                    maxScore = 0
                                    break
                                temp = score[prevTag, w-1] * self.__tagGivenTag(tag, prevTag)
                                if temp > maxScore:
                                    goodTag = prevTag
                                    maxScore = temp

                            score[index] = self.__wordGivenTag(word, tag)*maxScore
                            backPtr[index] = goodTag
                        w += 1

                    #Sequence Identification
                    #0 wasn't quite small enough
                    maxScore = -math.inf
                    #Using our unknown tag for placeholder.
                    lastTag = "/UKN"
                    for tag in potTags:
                        temp = score[(tag, len(words) - 1)]
                        if temp > maxScore:
                            maxScore = temp
                            lastTag = tag
                    seq.insert(0, lastTag)
                    #Iterating from second to last word backwards
                    for w in range(len(words) - 2, -1, -1):
                        bestTag = backPtr[(lastTag, w + 1)]
                        #populate the seq backwards, hope that is acceptable.
                        seq.insert(0, bestTag)
                        lastTag = bestTag

                    for i in range(len(seq)):
                        outp.write(words[i] + seq[i] + " ")
                        if i == (len(seq)-1):
                            outp.write("\n")

    #Makes list of tags a word has been seen as.
    def __getTagsForWords(self):
        wordTagDict = {}
        wordtags = list(self.__wordTagCounts.keys())
        for elem in wordtags:
            word, tag = elem.split('/')
            if word not in wordTagDict:
                wordTagDict[word] = []
            # Leaving the / makes things easier later on.
            wordTagDict[word].append('/' + tag)
        return wordTagDict

    @staticmethod
    def __removeExtra(line):
        index = line.rfind('/')
        if index == -1:
            return line
        return line[:index].replace('/', '') + line[index:]

    def __getCounts(self):
        tagDict = {}
        wordTagDict = {}
        tag4TagDict = {}
        firstTagDict = {}
        lineCount = 0
        with open(self.__file, 'r') as inp:
            for line in inp:
                lineCount += 1
                prevTag = ""
                words = line.split()
                for word in words:
                    if '/' in word:
                        tag = self.__removeExtra(word)
                        tag = tag[0:tag.rfind('/')] + tag[tag.rfind('/'):]
                        #Count occurrence of tags given a word.
                        if tag in wordTagDict:
                            wordTagDict[tag] += 1
                        else:
                            wordTagDict[tag] = 1
                        tag = tag[tag.rfind('/'):]
                        #Count occurrence of tags.
                        if tag in tagDict:
                            tagDict[tag] += 1
                        else:
                            tagDict[tag] = 1
                        # Count occurrence of tags starting a sentence.
                        if prevTag == "":
                            if tag in firstTagDict:
                                firstTagDict[tag] += 1
                            else:
                                firstTagDict[tag] = 1
                        #Count occurrence of tags given a previous tag.
                        else:
                            combTag = tag + prevTag
                            if combTag in tag4TagDict:
                                tag4TagDict[combTag] += 1
                            else:
                                tag4TagDict[combTag] = 1
                        prevTag = tag

        return wordTagDict, tagDict, tag4TagDict, firstTagDict, lineCount

    @staticmethod
    def getAccuracy(file):
        correct = 0
        wrong = 0
        with open(file, 'r') as orig:
            with open("POS.test.out", 'r') as pred:
                origLines = orig.readlines()
                predLines = pred.readlines()
                for i in range(min(len(origLines), len(predLines))):
                    origLine = origLines[i].split()
                    predLine = predLines[i].split()
                    #Not always the same length, use the smallest.
                    for j in range(min(len(origLine), len(predLine))):
                        if origLine[j] == predLine[j]:
                            correct += 1
                        else:
                            wrong += 1

                    wrong += max(len(origLine), len(predLine)) - min(len(origLine), len(predLine))  # really double check this bc i kind of suck at math

        return format((correct / (correct + wrong)) * 100, '.2f')

def main():
    if len(sys.argv) < 3:
        print("Too few input arguments")
        return
    AI = Viterbi(sys.argv[1])
    AI.predict(sys.argv[2])
    print(AI.getAccuracy(sys.argv[2]))


if __name__ == "__main__":
    main()
