import os
import re
import shutil
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-id", "--inputdir", required=True, help="Input existing directory that contains all cleaned html files.")
parser.add_argument("-od", "--outputdir", required=True, help="Output a new directory that will contain a new filepath structure for the cleaned html files.")
args = vars(parser.parse_args())

source = args["inputdir"]
destination = args["outputdir"]


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


def structure(dirname, newdirname):
    if not os.path.exists(newdirname):
        os.makedirs(newdirname)

    i = 1
    for root, dirs, files in os.walk(dirname):
        dirs.sort(key=natural_key)
        for f in tqdm(sorted(files, key=natural_key), ascii=True):
            if f.endswith('.html'):
                os.rename(os.path.join(root, f), str(i)+'.html')
                i += 1

    source = './'

    files1 = os.listdir(source)

    for fs in files1:
        if fs.endswith(".html"):
            shutil.move(fs, newdirname)


structure(source, destination)

