import sys

#For the first word
#Score function that calculates prob of a word given a tag * Prob of tag given previous tag (beginning sentence)
#backptr points to the tag that has given the current max probability

#For the rest of the words
#for each possible tag for one selected word
#prob of a word given a tag * Max of (Score of prev word * prob of tag given potential previous tag)
# - take the Max of the previous score * prob of Current known tag GIVEN a potential prev tag.
# - aka look thru list of tags the previous word could have been. Calculate these (*prevscore) and choose the largest one.
#Back pointer is updated with the tag from prev word that was chosen for max.
# - so if a noun had the highest max, store noun.

#We find the tag that yields the maximum score. So we have done this logic for each tag a word could be.
# - and now we find which of those had the highest score value, so we now know what tag should belong to this word
#For back pointer, we go back through
class Viterbi:

    def __init__(self, file):
        self.__file = file
        self.tagCounts = self.__getTagCounts()

    def removeTags(self):
        with open(self.__file, 'r') as inp:
            with open("POS.test.out", 'w') as outp:
                for line in inp:
                    newline = line
                    for i in range(len(line)):
                        tag = ""
                        if line[i] == '/':
                            temp = line[i:]
                            for char in temp:
                                if char != " ":
                                    tag = tag + char
                                else:
                                    break
                        newline = newline.replace(tag, "")
                    outp.write(newline)

    @staticmethod
    def __removeExtra(line):
        index = line.rfind('/')
        if index == -1:
            return line
        return line[:index].replace('/', '') + line[index:]

    def __getTagCounts(self):
        tagDict = {}
        with open(self.__file, 'r') as inp:
            for line in inp:
                words = line.split()
                for word in words:
                    if '/' in word:
                        tag = self.__removeExtra(word)
                        tag = tag[tag.rfind('/'):]
                        if tag in tagDict:
                            tagDict[tag] += 1
                        else:
                            tagDict[tag] = 1
        return tagDict


def main():
    if len(sys.argv) < 3:
        print("Too few input arguments")
        return

    test = Viterbi(sys.argv[1])
    #test.removeTags()
    for key, value in test.tagCounts.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
