#!/usr/bin/perl

use strict;

#!/usr/local/bin/perl

#use strict;

open(DEST, ">C:/perl_folder/signal_extract_v2.txt")

#----------------Containers-----------------------------------------------------
my $cont1="";
my $cont2="";

#----------------Variables------------------------------------------------------

#Name holders
my $entity_name="h_arch";
my $arch_name="behavioral";
my $compo_name="compo";

#IO holders
my @io_lines;       #raw IO data
my @io_list;        #list of IO names with comma
my @new_io_list;    #comma-separated list of IO names
my @io_type;        #info on in/out/inout
my $vector_list;    #info on vector (downto/to + range)
my $num_io;         #original no. of IO
my $new_num_io;     #no. of IO after comma-seperation

#frequency and time holders
my $clk_period="50ns";
my $freq_list;
#if asynchronous, frequency = -1
#should be able to contain nested frequencies for vectors
my $period_list;
my @duty_cy;
#should be able to contain nested duty cycle for vectors

push (@{$freq_list->[0][0]},"1000 hz");
push (@{$freq_list->[1][0]},"25000 hz");

#Line number holders
my $pos_entity;
my $pos_end;

#Temporary string holders
my $spare1="";
my $spare2="";
my $spare3="";
my $string;
my $temp;
my $tempA;
my $tempB;
my $line;
my @temp_array;
my @array;

#Counters
my $cnt_io;
my $cnt_up;
my $cnt_perm;       #permanent comma cnt
my $comma_cnt=0;    #temporary comma cnt
my $cnt1;
my $cnt2;
my $cnt3;
my $cnt_i;
my $cnt_j;


#----------------IO extraction--------------------------------------------------

if (open(MYFILE, "<C:/perl_folder/input.txt"))
{
    $line = <MYFILE>;
    $line = lc($line);
    while ($line ne "")
    {
        push (@array, $line);               #saving input into an array
        $line = <MYFILE>;
        $line = lc($line);
        $cnt1++;
    }
    #print @array;
close(MYFILE);
}

print "\n";
for (my $cnt2=0;$cnt2<$cnt1;$cnt2++)        #finding position of entity and end
{
    if ($array[$cnt2] =~ /entity/)
    {
        $temp=$cnt2+1;
        #print "Found 'entity' at Line $tempA\n";
        $pos_entity = $cnt2;
    }
    if ($array[$cnt2] =~ /architecture/)
    {
        $temp=$cnt2+1;
        #print "Found 'architecture' at Line $tempA\n";
    }
    if ($array[$cnt2] =~ /end/)
    {
        $temp=$cnt2+1;
        #print "Found 'end' at Line $tempA\n";
        if($cnt3==0)
        {
            $pos_end = $cnt2;
        }
        $cnt3++;
    }
}

$tempA=$pos_entity+1;
$tempB=$pos_end+1;

#print "\nI repeat: they are at Lines $tempA and $tempB\n\n";

for (my $cnt2=$pos_entity;$cnt2<($pos_end + 1);$cnt2++) #saving every line between entity and end into another array
{
    push (@io_lines, $array[$cnt2]);
}

for (my $cnt2=0;$cnt2<($pos_end - $pos_entity + 1);$cnt2++)
{
    #print $io_lines[$cnt2];
}

#print "\n";

for (my $cnt2=0;$cnt2<($pos_end - $pos_entity + 1);$cnt2++)
{

    $io_lines[$cnt2] =~ s/entity//;                 #filtering out the IO names
    $io_lines[$cnt2] =~ s/is//;
    $io_lines[$cnt2] =~ s/port\s{0,}\(//;
    $io_lines[$cnt2] =~ s/$entity_name//;
    $io_lines[$cnt2] =~ s/std_logic\s{0,}\);/std_logic/;
    $io_lines[$cnt2] =~ s/std_logic_vector\s{0,}\(\s{0,}\d+\s{0,}downto\s{0,}\d+\s{0,}\)\s{0,}\);/std_logic_vector \( downto \)/;
    $io_lines[$cnt2] =~ s/std_logic_vector\s{0,}\(\s{0,}\d+\s{0,}to\s{0,}\d+\s{0,}\)\s{0,}\);/std_logic_vector \( to \)/;
    $io_lines[$cnt2] =~ s/\s+//;
    $io_lines[$cnt2] =~ s/end//;
    #print "$io_lines[$cnt2]";

    #s/\(\d+\s{0,}downto\s{0,}\d+\)//;
}

$num_io=@io_lines;
$num_io -= 2;
print "Num IO is $num_io\n";

for (my $cnt2=0;$cnt2<($pos_end - $pos_entity - 1);$cnt2++)
{
    $io_lines[$cnt2]=$io_lines[$cnt2+1];
}

for (my $cnt2=0;$cnt2<($pos_end - $pos_entity - 1);$cnt2++)
{
    #print "$io_lines[$cnt2]\n";
}

#----------------Part 1: Name Filter--------------------------------------------

print "\n";

for($cnt_io=0;$cnt_io<$num_io;$cnt_io++)
{
    if ($cnt_io > 0)
    {
        $spare1=$spare1."\n".$spare2;   #for spacing
    }
    $spare3=$io_lines[$cnt_io];

    $spare3 =~ s/in//;
    $spare3 =~ s/out//;
    $spare3 =~ s/inout//;
    $spare3 =~ s/:+//;
    $spare3 =~ s/;+//;
    $spare3 =~ s/std_logic//;
    $spare3 =~ s/_vector//;
    $spare3 =~ s/\(\s{0,}\d+\s{0,}downto\s{0,}\d+\s{0,}\)//;
    $spare3 =~ s/\(\s{0,}\d+\s{0,}to\s{0,}\d+\s{0,}\)//;

    $spare3 =~ s/\s+//;

    if($spare3 =~ /,/) #counting the number of commas, hence additional inputs
    {
        $comma_cnt += ($spare3 =~ tr/,//);
        print "\nInitial comma_cnt is $comma_cnt\n";
    }

    $io_list[$cnt_io]=$spare3;
    #print $io_list[$cnt_io],"\n";
}

$new_num_io = $num_io + $comma_cnt;
print "New num IO is $new_num_io\n\n";

for($cnt_io=0;$cnt_io<$new_num_io;$cnt_io++)
{
    if(defined($io_list[$cnt_io]))
    {
        $io_list[$cnt_io] =~ s/\s+//;
        if($io_list[$cnt_io]=~ /,+/)
        {
            @temp_array = split(/,/,$io_list[$cnt_io]);
            push(@new_io_list,@temp_array);
        }
        else
        {
            push(@new_io_list,$io_list[$cnt_io]);
        }
    }
}

$new_num_io = @new_io_list;

for($cnt_io=0;$cnt_io<$new_num_io;$cnt_io++)
{
    #print "$new_io_list[$cnt_io]\n";
}

#----------------Part 2: IO type Filter-----------------------------------------

print "\n";
$comma_cnt=0;

for($cnt_io=0;$cnt_io<$new_num_io;$cnt_io++)
{
    #print "$cnt_io,$comma_cnt,$cnt_up,$cnt_perm\n";

    $spare3=$io_lines[$cnt_io];

    if($spare3 =~ /,/)
    {
        $comma_cnt = ($spare3 =~ tr/,//);
    }

    if($spare3 =~ /inout/)
    {
        $io_type[$cnt_io+$cnt_perm]="inout";
        if($comma_cnt > 0)
        {
            for($cnt_up=1;$cnt_up<=$comma_cnt;$cnt_up++)
            {
                $io_type[$cnt_io+$cnt_up+$cnt_perm]="inout";
            }
            $cnt_perm += $comma_cnt;
        }
    }
    elsif($spare3 =~ /in/)
    {
        $io_type[$cnt_io+$cnt_perm]="in";
        if($comma_cnt > 0)
        {
            for($cnt_up=1;$cnt_up<=$comma_cnt;$cnt_up++)
            {
                $io_type[$cnt_io+$cnt_up+$cnt_perm]="in";
            }
            $cnt_perm += $comma_cnt;

        }
    }
    elsif($spare3 =~ /out/)
    {
        $io_type[$cnt_io+$cnt_perm]="out";
        if($comma_cnt > 0)
        {
            for($cnt_up=1;$cnt_up<=$comma_cnt;$cnt_up++)
            {
                $io_type[$cnt_io+$cnt_up+$cnt_perm]="out";
            }
            $cnt_perm += $comma_cnt;

        }
    }

$comma_cnt=0;
}

for($cnt_io=0;$cnt_io<$new_num_io;$cnt_io++)
{
    print "$new_io_list[$cnt_io] => $io_type[$cnt_io]","\n";
}

#----------------Part 3: Vector Filter------------------------------------------
#Part 3: Std_logic or Vector filter. If Vector, keep range.

$spare3="";
$cnt_perm=0;
$comma_cnt=0;

print "\n";

for($cnt_io=0;$cnt_io<$new_num_io;$cnt_io++)
{
    $spare3=$io_lines[$cnt_io];

    if($spare3 =~ /,/)
    {
        $comma_cnt = ($spare3 =~ tr/,//);
    }

    if($spare3 =~ /vector/)
    {
        push (@{$vector_list->[$cnt_io+$cnt_perm]},1);

        if($spare3 =~ /downto/)
        {
            push (@{$vector_list->[$cnt_io+$cnt_perm]},"downto");
        }
        elsif($spare3 =~ /to/)
        {
            push (@{$vector_list->[$cnt_io+$cnt_perm]},"to");
        }

        while($spare3 =~ m/(\d+)/g)
        {
            push (@{$vector_list->[$cnt_io+$cnt_perm]},"$1");
        }

        if($comma_cnt > 0)
        {
            for($cnt_up=1;$cnt_up<=$comma_cnt;$cnt_up++)
            {
                push (@{$vector_list->[$cnt_io+$cnt_up+$cnt_perm]},1);
                if($spare3 =~ /downto/)
                {
                    push (@{$vector_list->[$cnt_io+$cnt_perm+$cnt_up]},"downto");
                }
                elsif($spare3 =~ /to/)
                {
                    push (@{$vector_list->[$cnt_io+$cnt_perm+$cnt_up]},"to");
                }

                while($spare3 =~ m/(\d+)/g)
                {
                    push (@{$vector_list->[$cnt_io+$cnt_perm+$cnt_up]},"$1");
                }
            }
            $cnt_perm += $comma_cnt;
        }
    }
    else
    {
        push (@{$vector_list->[$cnt_io+$cnt_perm]},0);
        if($comma_cnt > 0)
        {
            for($cnt_up=1;$cnt_up<=$comma_cnt;$cnt_up++)
            {
                push (@{$vector_list->[$cnt_io+$cnt_up+$cnt_perm]},0);
            }
            $cnt_perm += $comma_cnt;
        }
    }
    $comma_cnt=0;
}

for($cnt_i=0;$cnt_i<$new_num_io;$cnt_i++)
{
    for($cnt_j=0;$cnt_j<4;$cnt_j++)
    {
        if(defined($vector_list->[$cnt_i][$cnt_j]))
        {
            print "[$cnt_i][$cnt_j]: $io_type[$cnt_i] $new_io_list[$cnt_i] is $vector_list->[$cnt_i][$cnt_j]\n";
        }
    }
}

#----------------Container 1--------------------------------------------------
$spare1 = $spare2 = "";

$spare2="$new_num_io\n";

for ($cnt_io=0;$cnt_io<$new_num_io;$cnt_io++)
{
    $spare1="$io_type[$cnt_io]\n";
    $spare2=$spare2.$spare1;
}

for ($cnt_io=0;$cnt_io<$new_num_io;$cnt_io++)
{
    $spare1="$new_io_list[$cnt_io]\n";
    $spare2=$spare2.$spare1;
}

$cont1=$spare2;


print DEST $cont1;
close(DEST);
