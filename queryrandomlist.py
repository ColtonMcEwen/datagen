import re
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-if", "--inputfile", required=True, help="Input existing file that contains all the filepaths of the cleaned html files.")
parser.add_argument("-of", "--outputfile", required=True, help="Output a new file that will contain random duplicated 1, 2, 3, and 4 token words.")
args = vars(parser.parse_args())

source = args["inputfile"]
destination = args["outputfile"]


phrase_set = set()

fout = open(source, "r")
for line in fout:
    line = line.strip()

    with open(line, 'r') as myfile:
        data = myfile.read().replace('\n', ' ')

        # remove html tags
        data = re.sub('<[^<]+?>', '', data)

        # split into words
        tokens = data.split()

        # random token phrases
        # duplicate 1 token phrase
        for i in range(2):
            if len(tokens) > 1:
                rt = random.randrange(len(tokens)-1)
                a = tokens[rt]
            phrase_set.add(a)

        # duplicate 2 token phrases
        for i in range(2):
            if len(tokens) > 2:
                rt = random.randrange(len(tokens)-2)
                b = tokens[rt] + ' ' + tokens[rt + 1]
            phrase_set.add(b)

        # duplicate 3 token phrases
        for i in range(2):
            if len(tokens) > 3:
                rt = random.randrange(len(tokens)-3)
                c = tokens[rt] + ' ' + tokens[rt + 1] + ' ' + tokens[rt + 2]
            phrase_set.add(c)

        # duplicate 4 token phrases
        for i in range(2):
            if len(tokens) > 4:
                rt = random.randrange(len(tokens)-4)
                d = tokens[rt] + ' ' + tokens[rt+1] + ' ' + tokens[rt+2] + ' ' + tokens[rt+3]
            phrase_set.add(d)


outF = open(destination, "w")
for line in phrase_set:
  outF.write(line + "\n")
outF.close()

