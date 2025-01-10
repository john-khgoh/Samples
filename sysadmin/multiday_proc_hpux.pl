#!/usr/bin/perl
use strict;

#Get CPU & Memory info for 66.10 - 66.28, 34.142 - 34.145 (HPUX)

{
	my @outputs = ("66-10p2.txt","66-11p2.txt","66-12p2.txt","66-13p2.txt","66-14p2.txt","66-15p2.txt","66-16p2.txt","66-17p2.txt","66-18p2.txt","66-19p2.txt","66-20p2.txt","66-21p2.txt","66-22p2.txt","66-23p2.txt","66-24p2.txt","66-25p2.txt","66-26p2.txt","66-27p2.txt","66-28p2.txt","34-142p.txt","34-143p.txt","34-144p.txt","34-145p.txt","34-149p.txt","34-150p.txt","24-56p.txt","24-194p.txt","24-195p.txt","101-77p.txt","101-78p.txt","24-177p.txt","24-178p.txt","24-179p.txt","24-180p.txt","24-212p.txt","24-213p.txt","24-214p.txt"); #array containing output filenames
	my @inputs = ("66-10.txt","66-11.txt","66-12.txt","66-13.txt","66-14.txt","66-15.txt","66-16.txt","66-17.txt","66-18.txt","66-19.txt","66-20.txt","66-21.txt","66-22.txt","66-23.txt","66-24.txt","66-25.txt","66-26.txt","66-27.txt","66-28.txt","34-142.txt","34-143.txt","34-144.txt","34-145.txt","34-149.txt","34-150.txt","24-56.txt","24-194.txt","24-195.txt","101-77.txt","101-78.txt","24-177.txt","24-178.txt","24-179.txt","24-180.txt","24-212.txt","24-213.txt","24-214.txt"); #array containing input filenames
	my $cnt2;
	
	for($cnt2=0;$cnt2<40;$cnt2++)
	{
		open(DEST, ">C:/Users/john.kheng.hean.goh/Documents/CopyTo/Post/@outputs[$cnt2]") || die "$!"; #output
		my $cont="";
		my @array; #contains all the lines
		my $line; #contains one line at a time
		my $cnt_line; #num of lines
		my $cnt1; #general counter

		my $start_throw; #point until which to discard
		my $end_throw; #point after which to discard
		my $flag_s_throw=0;
		my $flag_e_throw=0;

		if (open(MYFILE, "C:/Users/john.kheng.hean.goh/Documents/CopyTo/@inputs[$cnt2]")) #input

		{
		$line = <MYFILE>;
		while ($line ne "")
		{
		push (@array, $line); #saving input into an array
		$line = <MYFILE>;
		$cnt_line++; #count the number of lines for the counter
		}
		}

		for($cnt1=0;$cnt1<$cnt_line;$cnt1++) #Find the starting and end points
		{
		if( @array[$cnt1] =~ /08:0[0-4]:0[0-9]/)
		{
		$start_throw = $cnt1;
		print "The start point is at line $start_throw\n";
		$flag_s_throw=1;
		}

		if( @array[$cnt1] =~ /16:0[0-4]:0[0-9]/)
		{
		$end_throw = $cnt1 + 1;
		print "The end point is at line $end_throw\n";
		$flag_e_throw=1;
		}
		}

		if ($flag_s_throw = 1) #Clearing every line before the starting point
		{
		for($cnt1=0;$cnt1<$start_throw;$cnt1++)
		{
		@array[$cnt1] = "";
		}
		}
		else
		{
		"The start point is not found!\n";
		}

		if ($flag_e_throw = 1) #Clearing every line after the ending point
		{
		for($cnt1=$end_throw;$cnt1<$cnt_line;$cnt1++)
		{
		@array[$cnt1] = "";
		}	
		}
		else
		{
		"The end point is not found!\n";
		}

		for($cnt1=$start_throw;$cnt1<$end_throw;$cnt1++)
		{
		#@array[$cnt1] =~ s/\s+/\t/;
		#@array[$cnt1] =~ s/\%/\t/g;
		#@array[$cnt1] =~ s/:/\t/g;
		
		@array[$cnt1] =~ s/://g; #new method variation 1
		@array[$cnt1] =~ s/\d+CPU//g;
		@array[$cnt1] =~ s/%//g;
		@array[$cnt1] =~ s/Mem/\t/;
		@array[$cnt1] =~ s/Disk\s+\d+//;
		}

		print DEST @array;

		close(DEST);
		close(MYFILE);
	}
}