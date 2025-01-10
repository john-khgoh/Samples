#!/usr/bin/perl
use strict;

#Get Memory info for 66.29 - 66.40 (Linux)

{
	my @outputs = ("New_MemoryUtil_17032013.txt","New_MemoryUtil_18032013.txt","New_MemoryUtil_19032013.txt","New_MemoryUtil_20032013.txt","New_MemoryUtil_21032013.txt","New_MemoryUtil_22032013.txt","New_MemoryUtil_23032013.txt","New_MemoryUtil_24032013.txt","New_MemoryUtil_25032013.txt","New_MemoryUtil_26032013.txt","New_MemoryUtil_27032013.txt","New_MemoryUtil_28032013.txt","New_MemoryUtil_29032013.txt","New_MemoryUtil_30032013.txt","New_MemoryUtil_31032013.txt","New_MemoryUtil_01042013.txt","New_MemoryUtil_02042013.txt","New_MemoryUtil_03042013.txt","New_MemoryUtil_04042013.txt","New_MemoryUtil_05042013.txt","New_MemoryUtil_06042013.txt","New_MemoryUtil_07042013.txt","New_MemoryUtil_08042013.txt","New_MemoryUtil_09042013.txt","New_MemoryUtil_10042013.txt","New_MemoryUtil_11042013.txt","New_MemoryUtil_12042013.txt","New_MemoryUtil_13042013.txt","New_MemoryUtil_14042013.txt","New_MemoryUtil_15042013.txt","New_MemoryUtil_16042013.txt","New_MemoryUtil_17042013.txt"); #array containing output filenames
	my @inputs = ("New_MemoryUtil_17032013.txt","New_MemoryUtil_18032013.txt","New_MemoryUtil_19032013.txt","New_MemoryUtil_20032013.txt","New_MemoryUtil_21032013.txt","New_MemoryUtil_22032013.txt","New_MemoryUtil_23032013.txt","New_MemoryUtil_24032013.txt","New_MemoryUtil_25032013.txt","New_MemoryUtil_26032013.txt","New_MemoryUtil_27032013.txt","New_MemoryUtil_28032013.txt","New_MemoryUtil_29032013.txt","New_MemoryUtil_30032013.txt","New_MemoryUtil_31032013.txt","New_MemoryUtil_01042013.txt","New_MemoryUtil_02042013.txt","New_MemoryUtil_03042013.txt","New_MemoryUtil_04042013.txt","New_MemoryUtil_05042013.txt","New_MemoryUtil_06042013.txt","New_MemoryUtil_07042013.txt","New_MemoryUtil_08042013.txt","New_MemoryUtil_09042013.txt","New_MemoryUtil_10042013.txt","New_MemoryUtil_11042013.txt","New_MemoryUtil_12042013.txt","New_MemoryUtil_13042013.txt","New_MemoryUtil_14042013.txt","New_MemoryUtil_15042013.txt","New_MemoryUtil_16042013.txt","New_MemoryUtil_17042013.txt"); #array containing input filenames
	my $cnt2;
	
	for($cnt2=0;$cnt2<50;$cnt2++)
	{
		open(DEST, ">C:/Users/john.kheng.hean.goh/Documents/CopyTo_2/158/RAM_Post/@outputs[$cnt2]") || die "$!"; #output
		my $cont="";
		my @array; #contains all the lines
		my $line; #contains one line at a time
		my $cnt_line; #num of lines
		my $cnt1; #general counter

		my $start_throw; #point until which to discard
		my $end_throw; #point after which to discard
		my $flag_s_throw=0;
		my $flag_e_throw=0;

		if (open(MYFILE, "C:/Users/john.kheng.hean.goh/Documents/CopyTo_2/158/RAM/@inputs[$cnt2]")) #input

		{
		$line = <MYFILE>;
		while ($line ne "")
		{
		push (@array, $line); #saving input into an array
		$line = <MYFILE>;
		$cnt_line++;
		}
		}

		for($cnt1=0;$cnt1<$cnt_line;$cnt1++) #Find the starting and end points
		{
		if( @array[$cnt1] =~ /0[7-9]:0[0-4]:0[0-4]/)
		{
		$start_throw = $cnt1;
		print "The start point is at line $start_throw\n";
		$flag_s_throw=1;
		}

		if( @array[$cnt1] =~ /1[5-7]:0[0-4]:0[0-4]/)
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
		
		@array[$cnt1] =~ s/\d+:\d+:\d+//g;
		}

		print DEST @array;

		close(DEST);
		close(MYFILE);
	}
}