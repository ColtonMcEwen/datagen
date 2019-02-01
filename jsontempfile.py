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

                        typetag = str(i % 10 + 1)
                        i += 1
                        type = """   "type": """ + "\"" + typetag + "\"" + "," + '\n'

                        companytag = str(j % 100 + 1)
                        j += 1
                        company = """   "company_name": """ + "\"" + companytag + "\"" + "," + '\n'

                        createdtag = str(k % 1000 + 1)
                        k += 1
                        createdbyname = """   "created_by_name": """ + "\"" + createdtag + "\"" + "," + '\n'

                        filexttag = str(m % 10000 + 1)
                        m += 1
                        filextension = """   "file_extension": """ + "\"" + filexttag + "\"" + "," + '\n'

                        filenatag = str(n % 100000 + 1)
                        n += 1
                        filename = """   "file_name": """ + "\"" + filenatag + "\"" + '\n' + "}"

                        wf = guid + name + description + url + type + company + createdbyname + filextension + filename

                        fout.write(wf + '\n')

            fin1.close()


    json(source, destination)

except OSError:
    sys.exit()
