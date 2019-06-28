import re
import os
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-id", "--inputdir", required=True, help="Input existing directory that contains all original html files.")
parser.add_argument("-od", "--outputdir", required=True, help="Output a new directory that will contain all cleaned html files.")
args = vars(parser.parse_args())

source = args["inputdir"]
destination = args["outputdir"]


def find_files(rawhtml, cleanedhtml):
    if os.path.exists(cleanedhtml):
        shutil.rmtree(cleanedhtml)
    shutil.copytree(rawhtml, cleanedhtml)

find_files(source, destination)


def cleanup(filename1):
    string = ""

    fin = open(filename1, 'r')
    for line in fin:
        line = re.sub('(&lt;)', '', line)
        line = re.sub('(<*.doc.*>)', '', line)
        line = re.sub('(".+")', '', line)
        line = re.sub('(a\shref=)', '', line)
        line = re.sub('(>,)', '>', line)
        line = re.sub('(&gt;)', '', line)
        line = re.sub('(/a)', '', line)
        line = re.sub('(&amp;ndash;)', '', line)
        string += line

    fin.close()
    return string


def write(filename2):
    text = cleanup(f1)
    fout = open(filename2, "w")
    for line in text:
        if line != "":
            fout.write(line)
    fout.close()


for root, dirs, filenames in os.walk(destination):
    for f in filenames:
        f1 = os.path.join(root, f)
        write(os.path.join(root, f))
