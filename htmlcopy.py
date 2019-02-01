import shutil
import argparse
import sys
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-if", "--inputfile", required=True, help="Input text file containing original html file paths.")
parser.add_argument("-if1", "--inputfile1", required=True, help="Input exisiting text file containing new html file paths.")
args = vars(parser.parse_args())

input = args["inputfile"]
input1 = args["inputfile1"]

try:
    def move(originalfilelist, newfilelist):
        i = 0
        fin1 = open(originalfilelist, "r")
        fin2 = open(newfilelist, "r")

        original = fin1.read().splitlines()
        new = fin2.read().splitlines()

        for file in tqdm(original, ascii=True):
            shutil.copyfile(file, new[i])
            i += 1


    move(input, input1)

except IndexError:
    sys.exit()
