import os
import urllib.parse
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-id", "--inputdir", required=True, help="Input existing directory that contains all cleaned html files.")
parser.add_argument("-of", "--outputfile", required=True, help="Output a new xml file that will contain URL links from all cleaned html filepaths.")
parser.add_argument("-u", "--url", required=True, help="Any URL to choose from as long as it has 'https://' before it.")
args = vars(parser.parse_args())

source = args["inputdir"]
destination = args["outputfile"]
url = args["url"]


def pathLinks(dirpath, pathname, urladdress):
    fout = open(pathname, "w")
    for root, dirs, filenames in os.walk(dirpath):
        for f in filenames:
            p = os.path.join(root, f)
            a = urllib.parse.urljoin(str(urladdress), p)
            b = "<url><loc>" + a + "</loc></url>"
            fout.write(b + '\n')
    fout.close()


pathLinks(source, destination, url)


