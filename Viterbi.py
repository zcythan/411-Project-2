#Insert Generic comment about system libraries being allowed
import sys

# For the first word
# Score function that calculates prob of a word given a tag * Prob of tag given previous tag (beginning sentence)
# backptr points to the tag that has given the current max probability

# For the rest of the words
# for each possible tag for one selected word
# prob of a word given a tag * Max of (Score of prev word * prob of tag given potential previous tag)
# - take the Max of the previous score * prob of Current known tag GIVEN a potential prev tag.
# - aka look thru list of tags the previous word could have been. Calculate these (*prevscore) and choose the largest one.
# Back pointer is updated with the tag from prev word that was chosen for max.
# - so if a noun had the highest max, store noun.

# We find the tag that yields the maximum score. So we have done this logic for each tag a word could be.
# - and now we find which of those had the highest score value, so we now know what tag should belong to this word
# For back pointer, we go back through
class Viterbi:

    def __init__(self, file):
        self.__file = file
        #Only read the file one time.
        self.__wordTagCounts, self.__tagCounts, self.tagForTagCounts, self.__startTagCounts, self.__lineCount = self.__getCounts()  # CHANGE THIS TO PRIVATE
        self.__tagsForWords = self.__getTagsForWords()

    #Calculates the probability a tag starts a sentence,
    #as there's no beginning of sentence tag in the data...
    def __tagStarts(self, tag):
        if self.__lineCount > 0:
            return self.__startTagCounts.get(tag, 0) / self.__lineCount
        return 0

    #Calculates the probability of a tag given a tag.
    def __tagGivenTag(self, tag, prevTag):
        return self.tagForTagCounts.get(tag+prevTag, 0)/self.__tagCounts.get(prevTag, 0)

    # Calculates the probability of word given a tag
    def __wordGivenTag(self, word, tag):
        return self.__wordTagCounts.get(word+tag, 0)/self.__tagCounts.get(tag, 0)

    def predict(self, file):
        with open(self.__file, 'r') as data:
            for line in data:
                init = True
                score = {}
                backPtr = {}
                words = line.split()
                for part in words:
                    if '/' in part:
                        full = self.__removeExtra(part)
                        # First half cast to lowercase, reduce duplicates.
                        word = tag[0:full.rfind('/')].lower()
                        #tag = tag[tag.rfind('/'):]
                        #Initialization
                        if init:
                            potTags = self.__tagsForWords.get(word, 0)
                            for tag in potTags:
                                score[0].append(tag, self.__wordGivenTag(word, tag) * self.__tagStarts(tag))
                                backPtr = 0

                            init = False


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

    def removeTags(self):
        with open(self.__file, 'r') as inp:
            with open("POS.test.out", 'w') as outp:
                for line in inp:
                    words = line.split()
                    tags = set(self.__tagCounts)
                    for i in range(len(words)):
                        for tag in tags:
                            if tag in words[i]:
                                words[i] = words[i].replace(tag, "")
                    outp.write(' '.join(words))

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
                        #First half cast to lowercase, reduce duplicates.
                        tag = tag[0:tag.rfind('/')].lower() + tag[tag.rfind('/'):]
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


def main():
    if len(sys.argv) < 3:
        print("Too few input arguments")
        return
    # train call
    # predict call
    test = Viterbi(sys.argv[1])
    #test.removeTags()
    print(test.tagGivenTag("/JJ", "/PP$"))

    for key, value in test.tagForTagCounts.items():
        print(f"{key} {value}")


if __name__ == "__main__":
    main()
