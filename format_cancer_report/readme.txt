##readme##
##2019-03-05
usage: format_cancer_report_v1.py [-h] -t {lung_56,options} -c CUSTOMER -d
                                  DATABASE [-o OUTPUT]
                                  directory

This script is to generate precisiongenes format cancer standard data from  tissue report .
All steps including targeting drug , chemotherapeutic drugs ,somatic mutation  ... 
Aim to get formate formatted file

Author : GuoqiLiu
Date   : 2019-02-28 14:25
Version: v1
Contact: liuguoqi@hmzkjy.cn  

positional arguments:
  directory             must input tissue report directory and at this
                        directory including XXX_germline_mutation.xls,XXX_hual
                        iao.xls,XXX_rate.xls,XXX_somatic_mutation2.xls four
                        file

optional arguments:
  -h, --help            show this help message and exit
  -t {lung_56,options}, --sample-type {lung_56,options}
                        select sample type what your gene detection eg :
                        lung_56,lung_8,colorectal_42 ... ,befor you input this
                        parameter you should know what gene detection has done
  -c CUSTOMER, --customer CUSTOMER
                        customer information including zkjy_ID zkjy_delegation
                        zkjy_acception zkjy_report zkjy_name zkjy_gender
                        zkjy_age zkjy_sample_type zkjy_clinical_info
                        zkjy_submission_unit,And they should be seperated by
                        Tab key,if you do not know any information please use
                        '/' instead
  -d DATABASE, --database DATABASE
                        database file has prepared by tissue department
                        colleague and you can use at the specified directory
  -o OUTPUT, --output OUTPUT
                        you can choose output file name and default
                        format_cancer_v1.txt
