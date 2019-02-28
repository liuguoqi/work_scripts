#!/usr/bin/perl -w 
###################################################################
####Author : GuoqiLiu                                             #
####Date   : 2019-02-25                                           #
####Copyright (C) 2018~2019 precisiongenes.com.cn                 #
####Contact: liuguoqi@hmzkjy.cn                                   #
####Suppose: add hg19 civic database to  somatic mutation file    #
####step :                                                        #
####1. Prepare hg19 civic database                                #
####2. Get tumour pipeline result somatic mutation file           #
####Platform :                                                    #
#############Centos7 & Windows10 ,Perl v5.16.3#####################
###################################################################

#log:
#20190225 end ;
#20190226 updated some mutation 
#
#
use strict ;
use warnings ;
use Getopt::Long;
use Cwd;
my %opts;
sub usage {
     my $VERSION = "V1.0";
     #my %opts;
     my $help ;
     my $current_dir = getcwd() ;
     GetOptions (\%opts,"i=s","c=s","o=s","h!"=> \$help) ;
     my $usage = <<"USAGE";
################################################################################################################
#         Usage:perl $0 [options] 
#         -h            Print help document and Exit 
#         -i*  <str>    somatic mutation from tissue pipeline result 
#         -c*  <str>    civic  database  annotation file   
#         -o   <str>    output file default : xxx_somatic_mutation3.xls
################################################################################################################
#         Example : $0 -i ZK90001112FFPE_somatic_mutation2.xls  -c hg19_civic_20190225.txt -o ZK90001112FFPE_somatic_mutation3.xls
################################################################################################################
#         Program : $0
#         Version : $VERSION
#         Contact : liuguoqi\@hmzkjy.cn
################################################################################################################
USAGE

die $usage if ( !$opts{i});
die $usage if ( !$opts{c});

#if ($help){&usage();exit;}
#set default argruments#
$opts{o} ||= "$current_dir/xxx_somatic_mutation3.xls"; ###output### 
##
}

usage();
##civic-chromosome  civic-start civic-stop  civic-reference_bases   civic-variant_bases civic-gene civic-variant    civic-variant_civic_url:civic-rating:civic-evidence_level:civic-disease:civic-drugs:civic-evidence_type:civic-evidence_direction:civic-clinical_significance:civic-variant_origin
##
sub get_current_time {
        my $head = shift ;
        chomp(my $current_date=`date "+%Y-%m-%d %H:%M:%S"`);
        print "###\@$current_date $head\n";
}
&get_current_time("now is reading civic hg19 database ...") ;
my %civic = () ;
open ANNOTATION,$opts{c}; 
while (<ANNOTATION>) {
       chomp;
       next if /^#/;
       my @annotation = split/\t/,$_;
       my $tmp = join("\t",@annotation[5..$#annotation]) ;
       push @{$civic{$annotation[0]."\t".$annotation[1]."\t".$annotation[3]."\t".$annotation[4]}},$tmp;
}

close ANNOTATION ;    

my $current_dir2 = getcwd() ;
open INPUT,$opts{i} ;
#$opts{c}
#open OUTPUT,">",$opts{o};
&get_current_time("now is reading somatic file ...") ;
open TMP,">",$current_dir2."/tmpfile" ; 
chomp(my $tmp = <INPUT>);
print TMP $tmp,"\traw_ref\traw_alt\n";
while (<INPUT>) {
        chomp;
        my @somatic = split/\t/,$_; 
        if (length($somatic[8]) <  length($somatic[9]))  {
                if (substr($somatic[9],0,length($somatic[8])) eq $somatic[8]) {
                        print TMP join("\t",@somatic[0..7]),"\t-\t",substr($somatic[9],length($somatic[8])),"\t",join("\t",@somatic[10..$#somatic]),"\t$somatic[8]\t$somatic[9]\n";
                }
                else {
                        print TMP join("\t",@somatic),"\t$somatic[8]\t$somatic[9]\n";
                }
        }
        elsif (length($somatic[8]) >  length($somatic[9])) {
                if (substr($somatic[8],0,length($somatic[9])) eq $somatic[9]) {
                        print TMP join("\t",@somatic[0..7]),"\t",substr($somatic[8],length($somatic[9])),"\t-\t",join("\t",@somatic[10..$#somatic]),"\t$somatic[8]\t$somatic[9]\n";
                }
                else {
                        print  TMP join("\t",@somatic),"\t$somatic[8]\t$somatic[9]\n";

                }
        }

       elsif (length($somatic[8]) ==  length($somatic[9])) {
               if ($somatic[8] ne $somatic[9]) {
                       print TMP join("\t",@somatic),"\t$somatic[8]\t$somatic[9]\n";
               }
               else {
                       print "Error $somatic[8] the length is equal $somatic[9] and $somatic[8] is $somatic[9]\n";
               }
       }

       else {
               print "Error please check it !!!\n";
       }
}
close INPUT;
close TMP;

#=head
&get_current_time("now is adding civic database to somatic file ...") ;
my %all = () ;
open MODIFY,$current_dir2."/tmpfile" ; 
#open OUTPUT,">",$opts{o};
open OUTPUT,">",$current_dir2."/tmpfile2" ;
chomp(my $head1 = <MODIFY>) ;
#print OUTPUT  $head1,"\tcivic-gene\tcivic-variant\tcivic-variant_civic_url:civic-rating:civic-evidence_level:civic-disease:civic-drugs:civic-evidence_type:civic-evidence_direction:civic-clinical_significance:civic-variant_origin\n";
while (<MODIFY>) {
        chomp;
		$all{$_} = 0;
        my @modify = split/\t/,$_;
        if ($modify[8] ne "-" && $modify[9] ne "-") {
                           #chr/start/ref/alt/
                if  (exists $civic{$modify[10]."\t".$modify[11]."\t".$modify[8]."\t".$modify[9]}) { 
                        foreach my $single (@{$civic{$modify[10]."\t".$modify[11]."\t".$modify[8]."\t".$modify[9]}}) {
                                print OUTPUT join("\t",@modify),"\t",$single,"\n";
                        }

                }
				else {
						 print OUTPUT join("\t",@modify),"\t","None\tNone\tNone\n";
				}
        }##if 8=9
        elsif ($modify[8] eq "-" && $modify[9] ne "-") {
                foreach my $single2 (keys %civic) {
                        my @array2 = split/\t/,$single2 ;
#if (($array2[2] eq "-") && ($array2[3] ne "-")&& (length($array2[3]) < length($modify[9])) &&  (substr($modify[9],0,length($array2[3])) eq $array2[3])) {print "$array2[2]|$array2[3]\t$modify[8]|$modify[9]||",substr($modify[9],0,length($array2[3])),"\n";}
                        if  (($array2[2] eq "-") && ($array2[3] ne "-") && ((length($array2[3]) > length($modify[9]))) && (substr($array2[3],0,length($modify[9])) eq $modify[9])){print "ref:$array2[2]|$array2[3]==$modify[8]|$modify[9]\n"; 
                                if (exists $civic{$modify[10]."\t".$modify[11]."\t".$array2[2]."\t".$array2[3]}) {
										foreach my $ok1 (@{$civic{$modify[10]."\t".$modify[11]."\t".$array2[2]."\t".$array2[3]}}) {
                                print  OUTPUT join("\t",@modify),"\t",$ok1,"\n";}}
								else {
										print OUTPUT join("\t",@modify),"\t","None\tNone\tNone\n";
								}
                   
               }#if which more##
                        elsif ($array2[2] eq "-" && $array2[3] ne "-" && (length($array2[3]) < length($modify[9])) && (substr($modify[9],0,length($array2[3])) eq $array2[3])){ 
                                if (exists $civic{$modify[10]."\t".$modify[11]."\t".$array2[2]."\t".$array2[3]}) {
										foreach my $ok2 (@{$civic{$modify[10]."\t".$modify[11]."\t".$array2[2]."\t".$array2[3]}}) {
                                print  OUTPUT join("\t",@modify),"\t",$ok2,"\n";} }
								else {
										print OUTPUT join("\t",@modify),"\t","None\tNone\tNone\n";
								}

                                               }#if which more##
                        elsif (($array2[2] eq "-") && (length($array2[3]) == length($modify[9])) && ($array2[3] eq $modify[9])) {

                                 if (exists $civic{$modify[10]."\t".$modify[11]."\t".$array2[2]."\t".$array2[3]}) {
										 foreach my $ok3 (@{$civic{$modify[10]."\t".$modify[11]."\t".$array2[2]."\t".$array2[3]}}) {
										                                 print  OUTPUT join("\t",@modify),"\t",$ok3,"\n";}}


#              print OUTPUT join("\t",@modify),"\t",$civic{$modify[10]."\t".$modify[11]."\t".$array2[2]."\t".$array2[3]},"\n";
                        }
                        else {
                                print OUTPUT join("\t",@modify),"\tNone\tNone\tNone\n"; 
                        }
          }#foreach 
        }##8 - 9 ATCG
        ######
        elsif ($modify[8] ne "-" && $modify[9] eq "-") {
                foreach my $single3 (keys %civic) {
                         my @array3 = split/\t/,$single3 ;
                         if  (($array3[2] ne "-") && ($array3[3] eq "-") && ((length($array3[2]) > length($modify[8]))) && (substr($array3[2],0,length($modify[8])) eq $modify[8])){ 
                                 if (exists $civic{$modify[10]."\t".$modify[11]."\t".$array3[2]."\t".$array3[3]}) {
										 foreach my $ii (@{$civic{$modify[10]."\t".$modify[11]."\t".$array3[2]."\t".$array3[3]}}) {                                                                                                       
                                 print  OUTPUT join("\t",@modify),"\t",$ii,"\n";}}
								 else {
										 print OUTPUT join("\t",@modify),"\tNone\tNone\tNone\n";
								 }
              }##if 
                        elsif ($array3[2] ne "-" && $array3[3] eq "-" && (length($array3[2]) < length($modify[8])) && (substr($modify[8],0,length($array3[2])) eq $array3[2])){
                                if (exists $civic{$modify[10]."\t".$modify[11]."\t".$array3[2]."\t".$array3[3]}) {
								
									foreach my $ii3 (@{$civic{$modify[10]."\t".$modify[11]."\t".$array3[2]."\t".$array3[3]}}) {
                                print  OUTPUT join("\t",@modify),"\t",$ii3,"\n";
								}} 
								
								else {
										print OUTPUT join("\t",@modify),"\tNone\tNone\tNone\n";
								}
              }##elsif 
						elsif ($array3[3] eq "-" && $array3[2] eq $modify[8]) {
								if (exists $civic{$modify[10]."\t".$modify[11]."\t".$array3[2]."\t".$array3[3]}) {
										foreach my $ii3 (@{$civic{$modify[10]."\t".$modify[11]."\t".$array3[2]."\t".$array3[3]}}){ print  OUTPUT join("\t",@modify),"\t",$ii3,"\n";}}
						}
				else {
						 print OUTPUT join("\t",@modify),"\tNone\tNone\tNone\n";
				}
		}##foreach
     }##elsif

#else {
#            print OUTPUT join("\t",@modify),"\t","None\tNone\tNone\n";
#       }
}


close MODIFY;
close OUTPUT;


#open O,">",$opts{o};
open O,">",$current_dir2."/tmpfile4";
`cat $current_dir2/tmpfile2 | sort |uniq  > $current_dir2/tmpfile3` ;
open I,$current_dir2."/tmpfile3" ;
#chomp(my $h1 = <I>);
#print O $h1,"\n";
print O  $head1,"\tcivic-gene\tcivic-variant\tcivic-variant_civic_url:civic-rating:civic-evidence_level:civic-disease:civic-drugs:civic-evidence_type:civic-evidence_direction:civic-clinical_significance:civic-variant_origin\n";

my %h=();
while (<I>) {
		chomp;
		my @b=split/\t/,$_;
#my $tmp=join("\t",@b[24..$#b]);
#		my $ky = join("\t",@b[0..23]);

        push @{$h{join("\t",@b[0..23])}} ,join("\t",@b[24..$#b]) ;
#										}
}
close I;
foreach my $i (keys %h) {
		        foreach my $jj (@{$h{$i}}) {
						if ($jj =~ /^None/) {
								next;
						}
						else {
								print O $i,"\t",$jj,"\n";
						}
				

				}}
close O;
my %good=();
open OO,">",$opts{o};
open II,$current_dir2."/tmpfile4";
my $hhh = <II> ;
print OO $hhh;
while (<II>) {
		chomp;
		my @ttt = split/\t/,$_;####0,23
		$good{join("\t",@ttt[0..23])} = join("\t",@ttt[24..$#ttt]) ;
}
close II;
foreach my $t1 (keys %all) {
		if (exists $good{$t1}) {
				print OO $t1,"\t",$good{$t1},"\n";
		}
		else {
				print  OO $t1,"\tNone\tNone\tNone\n";
		}
}
close OO;



`rm "$current_dir2/tmpfile"`;
`rm "$current_dir2/tmpfile2"`;
`rm "$current_dir2/tmpfile3"`;
`rm "$current_dir2/tmpfile4"`;
&get_current_time("now everything is ok please check it carefully ...") ;
