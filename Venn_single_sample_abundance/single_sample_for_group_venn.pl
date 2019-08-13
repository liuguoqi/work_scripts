#!/usr/bin/perl -w
#use strict;
use warnings;
use FindBin qw($Bin); 
die "perl $0 <venn.sets.xls>  <map.txt>  <otu_table.percent.xls|otu_table.xls.group.ok.txt>\n" if @ARGV!=3;

open I,$ARGV[0] ; 
chomp (my $h = <I>);

$h=~s/\&/-/g;
#print $h,"\n";
my @hh = split/\t/,$h;
my @samp;
foreach my $i (@hh) {
	if ($i =~ /only$/) 
	{
	$i=~s/\s+/__/g;
	push @samp,$i;
        }
	else 
	{
	$i=~s/\s+//g;
	push @samp,$i
        } 
}#
#print "@samp\n" ;
my %sam2v=();
for(my $t=0;$t <=$#samp;$t++) {
	$sam2v{$t} = $samp[$t] ;
}

open I2,$ARGV[1] ;
<I2>;
my @sam=();
while (<I2>) {
	chomp;
	my @a = split/\t/,$_;
	push @sam,$a[0] ;
}
close I2;

my %venn2otu=();

my %venn2otu2=();

while (<I>) {
	chomp;
         my @b = split/\t/,$_; 
	 foreach my $ii (@sam) {
		 for (my $j=0;$j <=$#b;$j++) {
			 $venn2otu2{$ii}{$sam2v{$j}} = 0;
			 if ($b[$j] eq "") {next;}
			 else {
			 push @{$venn2otu{$ii}{$sam2v{$j}}},$b[$j] ;}
		 }
	 }
 }
close I;
`perl /mnt/sdb/lgq/bin/tools/row2column.pl $ARGV[2] > $ARGV[2].tmp`;
 #foreach my $j (keys %venn2otu) {
 #	foreach my $j1 (keys %{$venn2otu{$j}}) { 
 #		print $j,"\t",$j1,"\t====>>>>>>@{$venn2otu{$j}{$j1}}\n";
 #	}
 #}
open I3,"$ARGV[2].tmp" ;
chomp (my $h3=<I3>) ;
my @h33=split/\t/,$h3;
my %otu2single=();
my %otu2index=();
for (my $z=1;$z<=$#h33;$z++) {
          $otu2index{$z} = $h33[$z] ;
  }
  while (<I3>) {
	  chomp;
	  my @cc=split/\t/,$_;
	  for (my $x=1;$x<=$#cc;$x++) {
		  $otu2single{$cc[0]}{$otu2index{$x}} = $cc[$x] ;
	  }
  }
  close I3;
  foreach my $j (keys %venn2otu) {
	  foreach my $j1 (keys %{$venn2otu{$j}}) { 
		  foreach my $ttt (@{$venn2otu{$j}{$j1}}) {
			  $venn2otu2{$j}{$j1} += $otu2single{$j}{$ttt} ;
		  }
	  }
  }

  print "#sample\t".join ("\t",@samp)."\n";
  foreach my $iz (@sam) {
	  print "$iz";
	  foreach my $izz (@samp) {
		  print "\t".$venn2otu2{$iz}{$izz};
	  }
	  print "\n";
  }




