import urllib.parse
import uuid
import re
import argparse
import sys
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-if", "--inputfile", required=True, help="Input existing file that contains a list of the cleaned html filepaths.")
parser.add_argument("-of", "--outputfile", required=True, help="Output a new file that will contain all json formatted content.")
args = vars(parser.parse_args())

source = args["inputfile"]
destination = args["outputfile"]

file1 = 'type.txt'
file2 = 'file_extension.txt'
file3 = 'company.txt'
file4 = 'name.txt'
file5 = 'filename.txt'


try:
    TAG_RE = re.compile(r'<[^>]+>')

    def natural_key(string_):
        return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]


    def json(filelist, newfile):
        i = 0
        j = 0
        k = 0
        m = 0
        n = 0

        with open(newfile, "w") as fout:
            fin1 = open(filelist, "r")
            for line in tqdm(fin1, ascii=True):
                line = line.strip()
                with open(line, 'r') as fin2:
                    rf = fin2.read()
                    r = rf.splitlines()
                    if rf != "":

                        guid = "{" + '\n' + """   "id": """ + "\"" + str(uuid.uuid4()) + "\"" + "," + '\n'

                        nametag = str(line)
                        nametag = TAG_RE.sub('', nametag)
                        name = """   "name": """ + "\"" + nametag + "\"" + "," + '\n'

                        descriptiontag = r[9:]
                        descriptiontag = TAG_RE.sub('', ' '.join(descriptiontag))
                        descriptiontag = re.sub(' {5}', ' ', descriptiontag)
                        descriptiontag = re.sub(' {3}', ' ', descriptiontag)
                        descriptiontag = re.sub(' {2}', ' ', descriptiontag)
                        descriptiontag = re.sub('"', r'\"', descriptiontag)
                        description = """   "description": """ + "\"" + descriptiontag + "\"" + "," + '\n'

                        urltag = urllib.parse.urljoin(str("http://test.fusioninfratest.com/"), line)
                        url = """   "url": """ + "\"" + urltag + "\"" + "," + '\n'

                        typeFile = open(file1, 'r')
                        typef = typeFile.read()
                        tf = typef.splitlines()

                        typetag = tf[i % 10]
                        i += 1
                        type = """   "type": """ + "\"" + typetag + "\"" + "," + '\n'

                        extensionFile = open(file2, 'r')
                        extensionf = extensionFile.read()
                        ef = extensionf.splitlines()

                        filexttag = ef[m % 100]
                        m += 1
                        filextension = """   "file_extension": """ + "\"" + filexttag + "\"" + "," + '\n'

                        companyFile = open(file3, 'r')
                        companyf = companyFile.read()
                        cf = companyf.splitlines()

                        companytag = cf[j % 1000]
                        j += 1
                        company = """   "company_name": """ + "\"" + companytag + "\"" + "," + '\n'

                        nameFile = open(file4, 'r')
                        namef = nameFile.read()
                        nf = namef.splitlines()

                        createdtag = nf[k % 10000]
                        k += 1
                        createdbyname = """   "created_by_name": """ + "\"" + createdtag + "\"" + "," + '\n'

                        filenameFile = open(file5, 'r')
                        filenamef = filenameFile.read()
                        ff = filenamef.splitlines()

                        filenatag = ff[n % 100000]
                        n += 1
                        filename = """   "file_name": """ + "\"" + filenatag + "\"" + '\n' + "}"

                        wf = guid + name + description + url + type + filextension + company + createdbyname + filename

                        fout.write(wf + '\n')

                        typeFile.close()
                        extensionFile.close()
                        companyFile.close()
                        nameFile.close()
                        filenameFile.close()

            fin1.close()

    json(source, destination)

except OSError:
    sys.exit()
