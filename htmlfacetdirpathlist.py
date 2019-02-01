import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-iname", "--inputname", required=True, help="Input name of new dataset directory.")
parser.add_argument("-inum", "--inputnum", required=True, help="Input number desired for the number of html files for new dataset directory to contain.")
parser.add_argument("-of", "--outputfile", required=True, help="Output new text file containing new file paths of html files.")
args = vars(parser.parse_args())

dsname = args["inputname"]
numf = args["inputnum"]
flist = args["outputfile"]


def printFiles(datasetname, numFiles, filelist):
    path = "/"
    for i in tqdm(range(numFiles), ascii=True):
        tens = i % 10 + 1
        hundreds = i % 100 + 1
        thousands = i % 1000 + 1
        tenThousands = i % 10000 + 1
        hundredThousands = i % 100000 + 1

        filepathfolder = str(datasetname) + path + str(tens) + path + str(hundreds) + path + str(thousands) + path + str(tenThousands) + path + str(hundredThousands)

        filepathlist = filepathfolder + path + str(i + 1) + ".html"

        outF = open(filelist, "a")
        outF.write(filepathlist + '\n')
        outF.close()


printFiles(str(dsname), int(numf), flist)
