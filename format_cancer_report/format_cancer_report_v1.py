#!/usr/bin/python3
##################################################################
###Author   : GuoqiLiu                                           #
###Date     : 2019-02-28                                         #
###Copyright (C) 2018~2019 precisiongenes.com.cn                 #
###Contact  : liuguoqi@hmzkjy.cn                                 #
###Suppose  : format automate cancer report data                 #
###Including:                                                    #
###(a).One probe corresponding more than one tissue :            #
###1. 90  genes (lung cancer,colorectal cancer ...)              #
###2. 56  genes (lung cancer, ...)                               #
###3. 42  genes ( ... )                                          #
###4. 618 genes ( ... )                                          #
###(b).Category :                                                #
###1.lung_8(meaning lung tissue 8 genes)/lung_11/lung_13/lung_56 #
###2.colorectal_42(meaning colorectal cancer 42 genes)           #
###3.thyroid_32/pancreatic_46/....                               # 
###Platform :                                                    #
###############Centos7 & Windows10 ,Python3.6+####################
##################################################################
###log     :first wrote_by_20190228 v1  first part only including lung 56 genes data 
###updated :  
import argparse
import textwrap
import re,os,sys,glob
__Author__='GuoqiLiu'
__Date__='20190301'
__Version__='v1'

mydir=os.getcwd()

def parse_command_line():
    '''this function is to parse command parameters'''
    description = """
           This script is to generate precisiongenes format cancer standard data from  tissue report .
           All steps including targeting drug , chemotherapeutic drugs ,somatic mutation  ... 
           Aim to get formate formatted file

           Author : GuoqiLiu
           Date   : 2019-02-28 14:25
           Version: v1
           Contact: liuguoqi@hmzkjy.cn  
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(description))
    parser.add_argument("directory", help="must input tissue report directory and at this directory including XXX_germline_mutation.xls,XXX_hualiao.xls,XXX_rate.xls,XXX_somatic_mutation2.xls four file")
    parser.add_argument("-t","--sample-type",choices = ['lung_56', 'options'],required=True,
                   dest="sample_type",type=str,help="select sample type what your gene detection eg : lung_56,lung_8,colorectal_42 ... ,befor you input this parameter you should know what gene detection has done")
    parser.add_argument('-c', '--customer',required=True,help="customer information including zkjy_ID\tzkjy_delegation\tzkjy_acception\tzkjy_report\tzkjy_name\tzkjy_gender\tzkjy_age\tzkjy_sample_type\tzkjy_clinical_info\tzkjy_submission_unit,And they should be seperated by Tab key,if you do not know any information please use '/' instead ")
    parser.add_argument('-d', '--database',help="database file has prepared by tissue department colleague and you can use at the specified directory",required=True,type=str)
    parser.add_argument('-o', '--output',help="you can choose output file name  and default format_cancer_v1.txt",default="format_cancer_v1.txt",type=str)
    args = parser.parse_args()
    return args
    #print ("this is a test {}...".format(args.directory))
    #print ("sampletype {}".format(args.sample_type))
argss=parse_command_line()#format(argss.sample_type)

class CustomerInfo() :
    '''
    this class in order to get customer infomatation and then print customer information to format_tissue.txt
    '''
    def __init__(self,zkjy_ID,zkjy_delegation,zkjy_acception,zkjy_report,zkjy_name,zkjy_gender,zkjy_age,zkjy_sample_type,zkjy_clinical_info,zkjy_submission_unit,outfile) :
        self.zkjy_ID=zkjy_ID
        self.zkjy_delegation=zkjy_delegation
        self.zkjy_acception=zkjy_acception
        self.zkjy_report=zkjy_report
        self.zkjy_name=zkjy_name
        self.zkjy_gender=zkjy_gender
        self.zkjy_age=zkjy_age
        self.zkjy_sample_type=zkjy_sample_type
        self.zkjy_clinical_info=zkjy_clinical_info
        self.zkjy_submission_unit=zkjy_submission_unit
        self.outfile=outfile
    def write_to_format_tissue(self) :
        '''
        this function is to customer infomatation write to format tissue .
        '''
        f=open(self.outfile,"w",encoding='utf-8')
        f.write(">Info\nzkjy_ID\tzkjy_delegation\tzkjy_acception\tzkjy_report\tzkjy_name\tzkjy_gender\tzkjy_age\tzkjy_sample_type\tzkjy_clinical_info\tzkjy_submission_unit\n")
        f.write(self.zkjy_ID+"\t"+self.zkjy_delegation+"\t"+self.zkjy_acception+"\t"+self.zkjy_report+"\t"+self.zkjy_name+"\t"+self.zkjy_gender+"\t"+str(self.zkjy_age)+"\t"+self.zkjy_sample_type+"\t"+self.zkjy_clinical_info+"\t"+self.zkjy_submission_unit+"\n")
        f.close()
        print (u"1.客户信息已整理完成!!!\n")
        #print ("1.customer information is succeed!\n")

def Read_customer_Information(csf) :
    customer_array=[]
    f1=open(csf,'r',encoding='utf-8')
    csfhead=f1.readline().rstrip()
    csfheada=csfhead.split("\t")
    csfi=f1.readline().rstrip()
    csfia=csfi.split("\t")
    if len(csfheada) != len(csfia) : 
        print (u"错误1：客户信息出错了请把客户的信息第一行和第二行对应起来")
        #print ("English : Please customer information first line and second line correspond !!")
        sys.exit(1)
    else :
        customer_array=csfia
    return customer_array
#if __name__=='__main__' :
def target_drug(inputdrug,tag=None) : 
    '''This function is to get target_drug resistant_drug by chr/pos/ref/alt/ by db.txt file '''
    tgd={}
    f2=open(inputdrug,'r',encoding='utf-8')
    f2.readline()
    init=1
    while init :
        line2=f2.readline().rstrip()
        if len(line2) == 0:
            break
        else :
            array2=line2.split("\t")
            if tag=="drug" :
                tgd[array2[0]+"\t"+array2[1]+"\t"+array2[2]+"\t"+array2[3]] = array2[4]+"\t"+array2[5]
            elif tag=="tips" :
                tgd[array2[8]]=array2[7]
            elif tag=="target_drug":
                tgd[array2[8]]=array2[9]+"\t"+array2[4]+"\t"+array2[10]+"\t"+array2[11]+"\t"+array2[6]
            elif tag=="study_drug":
                tgd[array2[8]]=array2[12]+"\t"+array2[13]+"\t"+array2[14]+"\t"+array2[15]
    f2.close()
    return tgd
tardrg = target_drug(argss.database,"drug")
gene2tipss = target_drug(argss.database,"tips")
tardrgg=target_drug(argss.database,"target_drug")
studydrg=target_drug(argss.database,"study_drug")
def get_customer_info() :
    info=Read_customer_Information(argss.customer)
    #print (argss.output)
    info.append(argss.output)
    #print (info)
    cus=CustomerInfo(info[0],info[1],info[2],info[3],info[4],info[5],info[6],info[7],info[8],info[9],info[10])
    cus.write_to_format_tissue()
get_customer_info()#general print customer information 
##lung_56/NCCN_11_genes##
NCCN11Genes=["EGFR","ALK","BRAF","ERBB2","KRAS","MET","RET","ROS1","NTRK1","NTRK2","NTRK3"]
nccn11=set(NCCN11Genes)
#print ("NCCN 11 genes : "+",".join(NCCN11Genes)+"...............\n")
Englist2Chinese={}
Englist2Chinese['missense_variant']="错义变异"
Englist2Chinese['frameshift_variant']="移码变异"
Englist2Chinese['splice_donor_variant']="剪切供体变异"
Englist2Chinese['conservative_inframe_insertion']="保守区域插入"
Englist2Chinese['disruptive_inframe_deletion']="破坏性删除"
Englist2Chinese['stop_gained']="终止增加"
Englist2Chinese['synonymous_variant']="同义突变"
##split#######ZK90001000PLA_somatic_mutation2.xls
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
        except Exception:
            print ("错误2：找不到体细胞突变的文件\n")
Split_somatic_mutation2(argss.directory)
#Split_somatic_mutation2
#################################################
def NCCN_11_genes(f3input,flag,labels):
    '''this function is to write lung_56/NCCN_11_genes ##argss.directory##'''
    myfile=glob.glob(f3input+"/*.xls*")
    for i in myfile :
        try :
            if i.endswith(flag):
                f3=open(i,"r",encoding='utf-8')
                f33=open(argss.output,"a",encoding='utf-8')
                f33.write(labels)
                #f33.write(">NCCN_11_genes\ngene\tmutation_1\tmutation_2\tmutation_3\tfrequency\ttarget_drug\tresistant_drug\n")
                _=f3.readline()
                while 1:
                    line3=f3.readline().rstrip()
                    if len(line3) == 0:
                        break
                    else :
                        array3=line3.split("\t")
                        f33.write(array3[1]+"\t"+array3[3]+"外显子"+array3[4]+"\t")
                        if array3[2] in Englist2Chinese :
                            f33.write(Englist2Chinese[array3[2]])
                        else :
                            f33.write(array3[2])
                        f33.write("\t"+array3[6]+"\t"+array3[5]+"\t")
                        if array3[10]+"\t"+array3[11]+"\t"+array3[8]+"\t"+array3[9] in tardrg :
                            f33.write(tardrg[array3[10]+"\t"+array3[11]+"\t"+array3[8]+"\t"+array3[9]]+"\n")
                        else :
                            f33.write("/\t/\n")
                f3.close()
                f33.close()
                print ("2.靶向药物检测结果整理完成!!!\n")
        except Exception :
            print ("错误2：没有找到体细胞突变的文件\n")
#labelss1=">NCCN_11_genes\ngene\tmutation_1\tmutation_2\tmutation_3\tfrequency\ttarget_drug\tresistant_drug\n"
#labelss2=">Other_45_genes\ngene\tmutation_1\tmutation_2\tmutation_3\tfrequency\ttarget_drug\tsentivity\n"
#NCCN_11_genes(argss.directory,".11genes",labelss1)
##(gene2tipss)
def somatic_gene2_tips(f33input,tag,labe):
    '''this function is to write lung_56/NCCN_11_genes ##argss.directory##'''
    myfile=glob.glob(f33input+"/*.xls*")
    for i in myfile :
        try :
            if i.endswith(tag):
                f3=open(i,"r",encoding='utf-8')
                f33=open(argss.output,"a",encoding='utf-8')
                f33.write(labe)
                #f33.write(">Clinical_tips_2_1\n")
                f33.write("num\tcontext\n")
                _=f3.readline()
                while 1:
                    line3=f3.readline().rstrip()
                    if len(line3) == 0:
                        break
                    else :
                        array3=line3.split("\t")
                        ii = 0
                        if array3[1] in gene2tipss :
                            ii+=1
                            f33.write(str(ii)+"\t"+gene2tipss[array3[1]]+"\n")
                        else :
                            print (array3[1],"这个基因没有对应的描述信息请检查一下,确认无误后可忽略本次警告信息"+"\n")
                f3.close()
                f33.close()
                print ("3.添加基因的描述文件已完成!!!\n")
        except Exception :
            print ("错误3：没有找到体细胞突变的文件\n")
leb1=">Clinical_tips_2_1\n"
leb2=">Clinical_tips_2_2\n"
labelss1=">NCCN_11_genes\ngene\tmutation_1\tmutation_2\tmutation_3\tfrequency\ttarget_drug\tresistant_drug\n"
labelss2=">Other_45_genes\ngene\tmutation_1\tmutation_2\tmutation_3\tfrequency\ttarget_drug\tsentivity\n"
NCCN_11_genes(argss.directory,".11genes",labelss1)
somatic_gene2_tips(argss.directory,".11genes",leb1)
NCCN_11_genes(argss.directory,".nongenes11",labelss2)
somatic_gene2_tips(argss.directory,".nongenes11",leb2)
############################################################
def target_summary(input4,tag):
    myfile=glob.glob(input4+"/*.xls")
    for i in myfile :
        try :
            if i.endswith("_somatic_mutation2.xls"):
                f4=open(i,"r",encoding='utf-8')
                f44=open(argss.output,"a",encoding='utf-8')
                f44.write(tag)
                _=f4.readline()
                while 1:
                    line4=f4.readline().rstrip()
                    if len(line4) == 0:
                        break
                    else :
                        array4=line4.split("\t")
                        if array4[1] in tardrgg :
                            f44.write(tardrgg[array4[1]]+"\n")
                        else :
                            pass
                print ("4.靶向药物汇总已完成!!!\n")
        except Exception :
            print ("错误4:靶向药小结出错了!!!\n")
tag11=">Target_drug\ndrug_EN\tdrug_CN\ttarget\tdisease\tSummary\n"
tag22=">Studying_drug\ndrug\ttarget\tintroduction\tsummary\n"
target_summary(argss.directory,tag11)
def target_summary2(input4,tag):
    myfile=glob.glob(input4+"/*.xls")
    for i in myfile :
        try :
            if i.endswith("_somatic_mutation2.xls"):
                f4=open(i,"r",encoding='utf-8')
                f44=open(argss.output,"a",encoding='utf-8')
                f44.write(tag)
                _=f4.readline()
                while 1:
                    line4=f4.readline().rstrip()
                    if len(line4) == 0:
                        break
                    else :
                        array4=line4.split("\t")
                        if array4[1] in studydrg :
                            f44.write(studydrg[array4[1]]+"\n")
                        else :
                            pass
                print ("5.在研究药物汇总已完结!!!\n")
        except Exception :
            print ("错误5:在研究药物小结出错了!!!\n")
target_summary2(argss.directory,tag22)
############################################################
def hualiao(input5):
    myfile=glob.glob(input5+"/*.xls")
    for i in myfile :
        try :
            if i.endswith("_hualiao.xls"):
                f4=open(i,"r",encoding='utf-8')
                f44=open(i+".tmp","w",encoding='utf-8')
                tag_=0
                while 1:
                    line4=f4.readline().rstrip()
                    tag_+=1
                    if len(line4) == 0:
                        break
                    else :
                        array4=line4.split("\t")
                        if 1<=tag_<=4:
                            f44.write("kabo\t"+line4+"\n")
                        elif 5<=tag_<=10:
                            f44.write("shunbo\t"+line4+"\n")
                        elif 11<=tag_<=14:
                            f44.write("yixi\t"+line4+"\n")
                        elif 15<=tag_<=17:
                            f44.write("jixi\t"+line4+"\n")
                        elif 18<=tag_<=21:
                            f44.write("duoxi\t"+line4+"\n")
                        elif 22<=tag_<=26:
                            f44.write("zishan\t"+line4+"\n")
                        elif tag_==27:
                            f44.write("changchun\t"+line4+"\n")
                        elif tag_==28:
                            f44.write("yituo\t"+line4+"\n")
                        elif 29<=tag_<=30:
                            f44.write("peimei\t"+line4+"\n")
                        else :
                            pass
                print ("6.化疗药物已汇总完成!!!\n")
        except Exception :
            print ("错误6(a):化疗药出错了!!!\n")
hualiao(argss.directory)
##################################################################################
def hualiao2(input6):
    myfile=glob.glob(input6+"/*.xls*")
    for i in myfile :
        try :
            if i.endswith("_hualiao.xls.tmp"):
                f4=open(i,"r",encoding='utf-8')
                f44=open(argss.output,"a",encoding='utf-8')
                f44.write(">Chemo_mutation\nchemo_drug\tsite\tresult\tgenotype\n")
                tag_=0
                while 1:
                    line4=f4.readline().rstrip()
                    tag_+=1
                    if len(line4) == 0:
                        break
                    else :
                        array4=line4.split("\t")
                        if array4[2] == "wild" :
                            f44.write(array4[0]+"\t"+array4[1]+"\t"+"野生型"+"\t"+array4[3]+"\n")
                        elif array4[2] == "HET" :
                            f44.write(array4[0]+"\t"+array4[1]+"\t"+"杂合型"+"\t"+array4[3]+"\n")
                        elif array4[2] == "HOM" :
                            f44.write(array4[0]+"\t"+array4[1]+"\t"+"纯合型"+"\t"+array4[3]+"\n")
                        else :
                            pass
        except Exception :
            print ("错误6(b):化疗药出错了!!!\n")
hualiao2(argss.directory)

def hualiao_drug(input7) :
    myfile=glob.glob(input7+"/*.xls")
    for i in myfile :
        try :
            if i.endswith("_rate.xls"):
                f4=open(i,"r",encoding='utf-8')
                f44=open(argss.output,"a",encoding='utf-8')
                f44.write(">Chemo_sentivity\nchemo_drug\tprediction\ttoxicity\n")
                tag_=0
                _=f4.readline()
                while 1:
                    line4=f4.readline().rstrip()
                    tag_+=1
                    if len(line4) == 0:
                        break
                    else :
                        array4=line4.split("\t")
                        arraytmp=[]
                        for ii in array4[1:]:
                            if ii == "ordinary" :
                                arraytmp.append("可能一般")
                            elif ii == "good" :
                                arraytmp.append("可能较好")
                            elif ii == "medium" :
                                arraytmp.append("可能中等")
                            elif ii== "high" :
                                arraytmp.append("可能很好")
                            elif ii== "NA" :
                                arraytmp.append("NA")
                            elif ii=="low" :
                                arraytmp.append("可能较低")
                            else :
                                print (ii+"这个表型还没有加入，请加入!!!\n")
                        if tag_==1:
                            f44.write("kabo\t"+"\t".join(arraytmp)+"\n")
                        elif tag_==2:
                            f44.write("shunbo\t"+"\t".join(arraytmp)+"\n")
                        elif tag_==3:
                            f44.write("yili\t"+"\t".join(arraytmp)+"\n")
                        elif tag_==4:
                            f44.write("jixi\t"+"\t".join(arraytmp)+"\n")
                        elif tag_==5:
                            f44.write("duoxi\t"+"\t".join(arraytmp)+"\n")
                        elif tag_==6:
                            f44.write("zishan\t"+"\t".join(arraytmp)+"\n")
                        elif tag_==7:
                            f44.write("changchun\t"+"\t".join(arraytmp)+"\n")
                        elif tag_==8:
                            f44.write("yituo\t"+"\t".join(arraytmp)+"\n")
                        elif tag_==9:
                            f44.write("peimei\t"+"\t".join(arraytmp)+"\n")
                        else :
                            pass
                print ("7.化疗药物整理已完成!!!\n")
        except Exception :
            print ("错误7：化疗药物整理出错了!!!\n")
hualiao_drug(argss.directory)
###############################################################
def germline_mutation(input8) :
    myfile=glob.glob(input8+"/*.xls")
    for i in myfile :
        try :
            if i.endswith("_germline_mutation.xls"):
                f4=open(i,"r",encoding='utf-8')
                f44=open(argss.output,"a",encoding='utf-8')
                f44.write(">Germine\ngene\tmutation_classification\tmutation\tmutation_type\tRisk\n")
                tag_=0
                _=f4.readline()
                while 1:
                    line4=f4.readline().rstrip()
                    tag_+=1
                    if len(line4) == 0:
                        break
                    else :
                        array4=line4.split("\t")
                        arraytmp=[]
                        arraytmp.append(array4[1])
                        if array4[2] == "intron_deletion" :
                            arraytmp.append("内含子缺失突变")
                        elif array4[2] == "missense_variant" :
                            arraytmp.append("错义变异")
                        elif array4[2] == "synonymous_variant" :
                                arraytmp.append("同义变异")
                        else :
                                arraytmp.append(array4[2])
                        arraytmp.append(array4[6])
                        if array4[22] == "HET" :
                            arraytmp.append("杂合性")
                        elif array4[22]== "HOM" :
                            arraytmp.append("纯合型")
                        else :
                            arraytmp.append(array4[22])
                        if array4[16] == "Benign":
                            arraytmp.append("良性")
                        else :
                            arraytmp.append(array4[16])
                        f44.write("\t".join(arraytmp)+"\n")
                print ("8.体细胞突变整理完成!!!\n")
        except Exception :
            print ("错误8：体细胞突变出错")
germline_mutation(argss.directory)
print ("全部完成了!!!\n")
