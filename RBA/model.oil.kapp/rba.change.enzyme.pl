#!/usr/bin/perl 
use strict;
#use FindBin qw($Bin/fdd_package/);
die "Usage: <part all>!\n"
unless @ARGV ;
my ($list_file,$xml)=@ARGV;
my %list;
######################################
&index(\%list,$list_file);
my $fun=<<in;
       <function id="NAME" type="constant" variable="growth_rate">
          <listOfParameters>
	     <parameter id="CONSTANT" value="VALUE"/>
	  </listOfParameters>
	</function>
in


my %stat;
open I,"$xml";
while(<I>){
	if(/<enzyme id="(R_\w*?_enzyme)/){
		my $zid=$1;
		#print "1\t$zid\n";
		if( exists $list{$zid}){
			#print "2\t$zid\n";
			s/forward_efficiency="default_efficiency"/forward_efficiency="${zid}_forward_efficiency"/;
			s/backward_efficiency="default_efficiency"/backward_efficiency="${zid}_backward_efficiency"/;
			print;
		}else{
			print;
		}
	}else{ print;}
}
close I;
##############################################################################
sub index{
	my ($hash,$file)=@_;
	open I,"$file";
	while(<I>){
		chomp;
		my @a=(split /\t/,);
		next unless $a[0] =~ /^R/;
		my $id ="$a[0]_enzyme";
		$$hash{ $id } = $a[2];
	}
	close I;
}
