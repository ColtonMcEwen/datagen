import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-if", "--inputfile", required=True, help="Input existing file that contains all the filepaths of the cleaned html files.")
args = vars(parser.parse_args())
source = args["inputfile"]

file1 = 'type.txt'
file2 = 'file_extension.txt'
file3 = 'company.txt'
file4 = 'name.txt'
file5 = 'filename.txt'

i = 0
j = 0
k = 0
m = 0
n = 0

try:
    count = 0
    fout = open(source, "r")
    for line in fout:
        line = line.strip()

        typeFile = open(file1, 'r')
        typef = typeFile.read()
        tf = typef.splitlines()

        typetag = tf[i % 10]
        i += 1

        extensionFile = open(file2, 'r')
        extensionf = extensionFile.read()
        ef = extensionf.splitlines()

        filexttag = ef[m % 100]
        m += 1

        companyFile = open(file3, 'r')
        companyf = companyFile.read()
        cf = companyf.splitlines()

        companytag = cf[j % 1000]
        j += 1

        nameFile = open(file4, 'r')
        namef = nameFile.read()
        nf = namef.splitlines()

        createdtag = nf[k % 10000]
        k += 1

        filenameFile = open(file5, 'r')
        filenamef = filenameFile.read()
        ff = filenamef.splitlines()

        filenatag = ff[n % 100000]
        n += 1

        with open(line, 'r+') as myfile:
            beginning = "<!DOCTYPE html>" + '\n' + "<html>" + '\n' + '\n' + "<head>" + '\n' + """<meta charset="UTF-8">""" + '\n' + "<meta name=" + "type " + "content=" + "\"" + typetag + "\""+ "/>" + '\n' + "<meta name=" + "file_extension " + "content=" + "\"" + filexttag + "\""+ "/>" + '\n' + "<meta name=" + "company_name " + "content=" + "\"" + companytag + "\""+ "/>" + '\n' + "<meta name=" + "created_by_name " + "content=" + "\"" + createdtag + "\""+ "/>" + '\n' + "<meta name=" + "file_name " + "content=" + "\"" + filenatag + "\""+ "/>" + '\n' + "<title>" + line + "</title>" + '\n' + "</head>" + '\n' + '\n' + "<body>"

            ending = '\n' + "</body>" + '\n' + "</html>"

            data = myfile.read()
            myfile.seek(0, 0)
            myfile.write(beginning.rstrip('\r\n') + data + ending)

            typeFile.close()
            extensionFile.close()
            companyFile.close()
            nameFile.close()
            filenameFile.close()

except OSError:
    sys.exit()
