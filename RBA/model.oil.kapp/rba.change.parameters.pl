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
	if(/<function id="(R_\w*?_enzyme)/){
		my $zid=$1;
		$stat{$zid}++;
		if( exists $list{$zid}){
			#print "$zid\t$list{$zid}\n";	
			print "$_";
			my $tmp=<I>; print "$tmp";
			my $tmp=<I>; #print "$tmp";
			print "\t<parameter id=\"CONSTANT\" value=\"$list{$zid}\"/>\n";
			my $tmp=<I>; print "$tmp";
			my $tmp=<I>; print "$tmp";
		}else{
			print "$_";
			#my $tmp=<I>; print "$tmp";
			#my $tmp=<I>; #print "$tmp";
			#$tmp=~ /value=\"(\S*?)\"/; my $value=$1;
			#if($value <5770){
			#	print "\t<parameter id=\"CONSTANT\" value=\"5770\"/>\n";
			#}else{
			#	print "$tmp";
				#}
				#my $tmp=<I>; print "$tmp";
				#my $tmp=<I>; print "$tmp";
		}
	}elsif(/<\/listOfFunctions>/){
		foreach my $zid( keys %list){
			unless(exists $stat{$zid}){
				#print "ADD.$zid\n";

				my $add=$fun;
				my $id="${zid}_forward_efficiency";
				$add=~ s/NAME/$id/;
				$add=~ s/VALUE/$list{$zid}/;
				print "$add";

				my $add=$fun;
				my $id="${zid}_backward_efficiency";
				$add=~ s/NAME/$id/;
				$add=~ s/VALUE/$list{$zid}/;
				print "$add";
			}
		}
		print "<\/listOfFunctions>\n";
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
		#if($a[2] <5770){$a[2] = 5770;}
		$$hash{ $id } = $a[2];
	}
	close I;
}
