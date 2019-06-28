from itertools import zip_longest
import os, tempfile
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-if", "--inputfile", required=True, help="Input existing xml file that contains a list of links with filepaths of the cleaned html files.")
args = vars(parser.parse_args())

source = args["inputfile"]


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


n = 50000


def generator(filename):
    beginning = """<?xml version="1.0" encoding="UTF-8"?>""" + '\n' + """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""
    with open(filename) as f:
        for i, g in enumerate(grouper(n, f, fillvalue=None)):
            with tempfile.NamedTemporaryFile('r+', delete=False) as fout:
                fout.write(beginning.rstrip('\r\n') + '\n')
                for j, line in enumerate(g, 1): # count number of lines in group
                    if line is None:
                        j -= 1 # don't count this line
                        break
                    fout.write(line)

                ending = "</urlset>"
                fout.seek(0, 2)
                fout.write(ending.rstrip('\r\n'))
            os.rename(fout.name, 'sitemap{0}.xml'.format(i + 1))


generator(source)
