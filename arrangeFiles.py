import os, shutil, glob, sys
import io
import csv
import re
import locale

#print (locale.getpreferredencoding())

dataDir = r'G:\Downloads\Stadtarchiv Wertheim\S-N 70_Glasplattenauswahl_CdV_JPGs'
kategorienDatei = r'G:\Downloads\Stadtarchiv Wertheim\cdvbw22_wertheim_kategorien.tsv'
#,encoding="utf-8"
#stdout_encoding = sys.stdout.encoding or sys.getfilesystemencoding()
stdout_encoding = sys.stdout.encoding #locale.getpreferredencoding()
print("std encoding: " + stdout_encoding)

bilderKategorienDatei = r'G:\Downloads\Stadtarchiv Wertheim\bilderKategorienMap.tsv'

with io.open(kategorienDatei, "r", encoding="utf-8") as file:
    kategorien = file.readlines()
#    kategorien = [line.rstrip().decode("utf-8").encode("ascii", 'ignore').decode("ascii") for line in kategorien]
    kategorien = [line.rstrip().encode(stdout_encoding, 'ignore') for line in kategorien]

for k in kategorien:
    dirName = str('').encode(stdout_encoding, 'ignore')
    try:
        dirName = k.encode( stdout_encoding , 'ignore' )

        if os.path.exists(dataDir+"\\"+dirName):
            print(">>" + dirName.decode("UTF-8").encode('ascii') + "<< gibt es schon!")
        else:
            os.mkdir(dataDir+"\\"+dirName)
    except Exception as e:
        print(str(e) + " during " + dirName)
l = 0
bilderKategorienMap = {}
with open(bilderKategorienDatei, 'r') as fd:
    reader = csv.reader(fd, delimiter = '\t')
    if l > 10:
        exit(1)
    for row in reader:
        # do something
        bilderKategorienMap.update({row[4]: row[1].encode(stdout_encoding, 'ignore')})
    l = l + 1


for f in glob.glob(dataDir+'\\*.jpg'):
    m = re.search(r'S-N 70_G (.+)_[0-9]{4,4}[a-d]*\.jpg', f)
    try:
        subFolder = bilderKategorienMap.get(m.group(1))
        #print("Verschiebe Datei >> "+f+" << in den Ordner "+subFolder)
        head, tail = os.path.split(f)
        os.rename(f, dataDir+"\\"+subFolder+"\\"+tail)
        print("Datei alt: "+f)
        print("Datei neu: "+dataDir+"\\"+subFolder+"\\"+tail)
    except Exception as e:
        print("ach nee doch nicht"+ str(e))
        print(f)
        print("fehlerhafter Folder: "+subFolder)
        #os.mkdir(dataDir+"\\"+subFolder)


#print(bilderKategorienMap)