import xlrd
import sys
import re
#import codecs

def usage() :
    print ("Error : please input <xxx.xlsx> <outputfile>\n")


if len(sys.argv) != 3:
    usage()
    raise SystemExit


#print (sys.argv)


data = xlrd.open_workbook(sys.argv[1])

table = data.sheets()[0]
nrows = table.nrows
file = open(sys.argv[2],"w",encoding="utf-8")
for i in range(nrows):
    array=[]
    l = table.row_values(i)
    #file.write("\t".join(str(l))+"\n")
    for k in l:
        k=str(k)
        array.append(k)
    file.write("\t".join(array)+"\n")
