#Author  : GuoqiLiu
#Date    : 2019-02-27
#Suppose : add civic database to somatic mutation
This script is to add civic database to somatic mutation
script useguide :

################################################################################################################
#         Usage:perl add_civic_annot_somatic_mutation.pl [options] 
#         -h            Print help document and Exit 
#         -i*  <str>    somatic mutation from tissue pipeline result 
#         -c*  <str>    civic  database  annotation file   
#         -o   <str>    output file default : xxx_somatic_mutation3.xls
################################################################################################################
#         Example : add_civic_annot_somatic_mutation.pl -i somatic_mutation2.xls  -c hg19_civic_20190225.txt
################################################################################################################
#         Program : add_civic_annot_somatic_mutation.pl
#         Version : V1.0
#         Contact : liuguoqi@hmzkjy.cn
################################################################################################################
