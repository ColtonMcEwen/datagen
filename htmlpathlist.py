import os
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-id", "--inputdir", required=True, help="Input existing directory that contains all cleaned html files.")
parser.add_argument("-of", "--outputfile", required=True, help="Output a new file that will contain all the filepaths of the cleaned html files.")
args = vars(parser.parse_args())

source = args["inputdir"]
destination = args["outputfile"]


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def pathList(word_file):
    for root, dirs, files in os.walk(word_file):
        dirs.sort(key=natural_key)
        for f in sorted(files, key=natural_key):
            if f.endswith('.html'):
                list_set = os.path.join(root, f)

                outF = open(destination, "a")
                outF.write(list_set + '\n')
                outF.close()

pathList(source)
