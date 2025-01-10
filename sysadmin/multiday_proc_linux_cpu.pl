#!/usr/bin/perl
use strict;

#Get CPU info(Linux)

{
	my @outputs = ("CPUUtil_12032013.txt","CPUUtil_14032013.txt","CPUUtil_15032013.txt","CPUUtil_17032013.txt","CPUUtil_18032013.txt","CPUUtil_19032013.txt","CPUUtil_20032013.txt","CPUUtil_21032013.txt","CPUUtil_22032013.txt","CPUUtil_23032013.txt","CPUUtil_24032013.txt","CPUUtil_25032013.txt","CPUUtil_26032013.txt","CPUUtil_27032013.txt","CPUUtil_28032013.txt","CPUUtil_29032013.txt","CPUUtil_30032013.txt","CPUUtil_31032013.txt","CPUUtil_01042013.txt","CPUUtil_02042013.txt","CPUUtil_03042013.txt","CPUUtil_04042013.txt","CPUUtil_05042013.txt","CPUUtil_06042013.txt","CPUUtil_07042013.txt","CPUUtil_08042013.txt","CPUUtil_09042013.txt","CPUUtil_10042013.txt","CPUUtil_11042013.txt","CPUUtil_12042013.txt","CPUUtil_13042013.txt","CPUUtil_14042013.txt","CPUUtil_15042013.txt","CPUUtil_16042013.txt","CPUUtil_17042013.txt"); #array containing output filenames
	my @inputs = ("CPUUtil_12032013.txt","CPUUtil_14032013.txt","CPUUtil_15032013.txt","CPUUtil_17032013.txt","CPUUtil_18032013.txt","CPUUtil_19032013.txt","CPUUtil_20032013.txt","CPUUtil_21032013.txt","CPUUtil_22032013.txt","CPUUtil_23032013.txt","CPUUtil_24032013.txt","CPUUtil_25032013.txt","CPUUtil_26032013.txt","CPUUtil_27032013.txt","CPUUtil_28032013.txt","CPUUtil_29032013.txt","CPUUtil_30032013.txt","CPUUtil_31032013.txt","CPUUtil_01042013.txt","CPUUtil_02042013.txt","CPUUtil_03042013.txt","CPUUtil_04042013.txt","CPUUtil_05042013.txt","CPUUtil_06042013.txt","CPUUtil_07042013.txt","CPUUtil_08042013.txt","CPUUtil_09042013.txt","CPUUtil_10042013.txt","CPUUtil_11042013.txt","CPUUtil_12042013.txt","CPUUtil_13042013.txt","CPUUtil_14042013.txt","CPUUtil_15042013.txt","CPUUtil_16042013.txt","CPUUtil_17042013.txt"); #array containing input filenames
	my $cnt2;
	
	#RT2 variables
	my $result;
	my $d1,my $d2,my $d3,my $d4, my $d5,my $d6;
	my $fd1, my $fd2, my $fd3;
	
	for($cnt2=0;$cnt2<50;$cnt2++)
	{
		open(DEST, ">C:/Users/john.kheng.hean.goh/Documents/CopyTo_2/158/CPU_Post/@outputs[$cnt2]") || die "$!"; #output
		my $cont="";
		my @array; #contains all the lines
		my $line; #contains one line at a time
		my $cnt_line; #num of lines
		my $cnt1; #general counter

		my $start_throw; #point until which to discard
		my $end_throw; #point after which to discard
		my $flag_s_throw=0;
		my $flag_e_throw=0;

		if (open(MYFILE, "C:/Users/john.kheng.hean.goh/Documents/CopyTo_2/158/CPU/@inputs[$cnt2]")) #input

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
		if( @array[$cnt1] =~ /0[7-9]:0[0-5]:0[0-5]/)
		{
		$start_throw = $cnt1;
		print "The start point is at line $start_throw\n";
		$flag_s_throw=1;
		}

		if( @array[$cnt1] =~ /1[5-7]:0[0-5]:0[0-5]/)
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
		
		@array[$cnt1] =~ s/\d+:\d+:\d+//g; #new method variation 2
		@array[$cnt1] =~ /(\d+).(\d)(\d)\s+(\d+).(\d)(\d)/;
		
		$d1=$1; 
		$d2=$2;
		$d3=$3;
		$d4=$4;
		$d6=$6;
		$d5=$5;
		
		$fd1=$d1+$d4; #adding the digits
		$fd2=$d2+$d5;
		$fd3=$d3+$d6;
		
		if($fd3>= 10) #3rd digit carry over
		{
			$fd2+=1;
			$fd3-=10;
		}
		if($fd2>= 10) #2nd digit carry over
		{
			$fd1+=1;
			$fd2-=10;
		}
		
		@array[$cnt1] = "$fd1.$fd2$fd3\n";
		}

		print DEST @array;

		close(DEST);
		close(MYFILE);
	}
}