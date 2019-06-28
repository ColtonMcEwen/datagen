from itertools import zip_longest
import os, tempfile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-if", "--inputfile", required=True, help="Input existing file that contains all json formatted content.")
args = vars(parser.parse_args())

source = args["inputfile"]


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


n = 11


def generator(filename):
    with open(filename) as f:
        for i, g in enumerate(grouper(n, f, fillvalue=None)):
            with tempfile.NamedTemporaryFile('r+', delete=False) as fout:
                for j, line in enumerate(g, 1): # count number of lines in group
                    if line is None:
                        j -= 1 # don't count this line
                        break
                    fout.write(line)
            os.rename(fout.name, '{0}.json'.format(i + 1))


generator(source)
