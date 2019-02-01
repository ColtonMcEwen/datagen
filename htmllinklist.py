import os
import re
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-id", "--inputdir", required=True, help="Input existing directory that contains all cleaned html files.")
parser.add_argument("-of", "--outputfile", required=True, help="Output a new file that will contain URL links from all cleaned html filepaths.")
args = vars(parser.parse_args())

source = args["inputdir"]
destination = args["outputfile"]


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def linkList(dirpath, pathname):
    fout = open(pathname, "w")
    for root, dirs, filenames in os.walk(dirpath):
        dirs.sort(key=natural_key)
        for f in tqdm(sorted(filenames, key=natural_key), ascii=True):
            p = os.path.join(root, f)
            b = "<a href=" + "\"" + "/" + p + "\">" + "/" + p + "</a>"
            fout.write(b + '\n')
    fout.close()

linkList(source, destination)
