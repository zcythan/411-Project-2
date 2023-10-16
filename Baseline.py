import sys

#Assigns each word a tag based on highest observed frequency in training data.
class Baseline:
    def __init__(self, file):
        self.__file = file
        self.__wordTagCounts = self.__getCounts()

    @staticmethod
    def __removeExtra(line):
        index = line.rfind('/')
        if index == -1:
            return line
        return line[:index].replace('/', '') + line[index:]

    def predict(self, file):
        with open(file, 'r') as data:
            with open("Baseline.test.out", 'w') as outp:
                for line in data:
                    wordsRaw = line.split()
                    words = []
                    seq = []
                    for part in wordsRaw:
                        word = part[0:part.rfind('/')]
                        words.append(word)
                    for word in words:
                        freq = 0
                        #Using same unknown tag placeholder
                        tag = "/UNK"
                        if word in self.__wordTagCounts:
                            for curTag, curFreq in self.__wordTagCounts[word].items():
                                if curFreq > freq:
                                    freq = curFreq
                                    tag = curTag

                        seq.append(word + tag)

                    for i in range(len(seq)):
                        outp.write(seq[i] + " ")
                        if i == (len(seq) - 1):
                            outp.write("\n")

    def __getCounts(self):
        wordTagDict = {}
        with open(self.__file, 'r') as inp:
            for line in inp:
                words = line.split()
                for fullWord in words:
                    if '/' in fullWord:
                        tag = self.__removeExtra(fullWord)
                        word = tag[0:tag.rfind('/')]
                        tag = tag[tag.rfind('/'):]
                        #Count occurrence of tags given a word.
                        #I optimized this to use nested dictionaries here,
                        #I think if I were to redo Viterbi.py I would have used this approach.
                        #I was trying to get clever by leaving the strings concatenated but never-
                        # -really ended up taking advantage of it.
                        if word in wordTagDict:
                            if tag in wordTagDict[word]:
                                wordTagDict[word][tag] += 1
                            else:
                                wordTagDict[word][tag] = 1
                        else:
                            wordTagDict[word] = {}
                            wordTagDict[word][tag] = 1
        return wordTagDict

    @staticmethod
    def getAccuracy(file):
        correct = 0
        wrong = 0
        with open(file, 'r') as orig:
            with open("Baseline.test.out", 'r') as pred:
                origLines = orig.readlines()
                predLines = pred.readlines()
                #ensure smallest used incase length isn't equal.
                for i in range(min(len(origLines), len(predLines))):
                    origLine = origLines[i].split()
                    predLine = predLines[i].split()
                    for j in range(min(len(origLine), len(predLine))):
                        if origLine[j] == predLine[j]:
                            correct += 1
                        else:
                            wrong += 1
        return format((correct / (correct + wrong)) * 100, '.2f')


def main():
    if len(sys.argv) < 3:
        print("Too few input arguments")
        return
    AI = Baseline(sys.argv[1])
    AI.predict(sys.argv[2])
    print(AI.getAccuracy(sys.argv[2]))


if __name__ == "__main__":
    main()