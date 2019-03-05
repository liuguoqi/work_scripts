import glob
def Split_somatic_mutation2(dir_somatic_mutation2):
    myfile2=glob.glob(dir_somatic_mutation2+"/*.xls")
    for j in myfile2 :
        try :
            if j.endswith("_somatic_mutation2.xls"):
                ftmp=open(j,"r",encoding='utf-8')
                ftmp2=open(j+".11genes","w",encoding='utf-8')
                ftmp22=open(j+".nongenes11","w",encoding='utf-8')
                head_1=ftmp.readline()
                ftmp2.write(head_1)
                ftmp22.write(head_1)
                while True : 
                    linetmp=ftmp.readline().rstrip()
                    if len(linetmp) == 0 :
                        break
                    else :
                        linetmparray=linetmp.split("\t")
                        if linetmparray[1] in nccn11 :
                            ftmp2.write("\t".join(linetmparray)+"\n")
                        else :
                            ftmp22.write("\t".join(linetmparray)+"\n")
                ftmp.close()
                ftmp2.close()
                ftmp22.close()
        except Exception :
            print ("找不到文件！！！！！")
Split_somatic_mutation2("/share/liuguoqi/bin/script/format_cancer_report")
