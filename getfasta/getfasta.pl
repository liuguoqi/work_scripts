#!/usr/bin/perl -w
###################################################################
####Author : GuoqiLiu                                             #
####Date   : 2019-01-14                                           #
####Copyright (C) 2018~2019 precisiongenes.com.cn                 #
####Contact: liuguoqi@hmzkjy.cn                                   #
####Suppose : get fasta file from a big fasta file                #
####Platform :                                                    #
#############Centos7 & Windows10 ,Perl v5.16.3#####################
###################################################################
use strict; 
use warnings;
die "perl $0 <fastafile> <list> <output>\n"  if @ARGV!=3 ;

my %getfasta = () ;
open LIST,$ARGV[1] ;
while(<LIST>) {
     chomp;
     $getfasta{">".$_} = 0 ; 
}
close LIST ;

my $tag = 0 ;
open FASTAFILE ,$ARGV[0] ;

open OUTPUT,">",$ARGV[2] ;
while (<FASTAFILE>) {
       chomp; 
       if (/^>/) {
            if (exists $getfasta{$_}) { 
                $tag = 1 ; 
                #print $_ ,"\n" ;
               }
            else {
                $tag = 0 ;
               }
      }
        print OUTPUT "$_\n" if $tag == 1; 
}

close FASTAFILE;
close OUTPUT ;
