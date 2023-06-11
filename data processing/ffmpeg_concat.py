#Script to concatenate video files in the "input" directory using FFMPEG
#Requires FFMPEG to be installed and added to path prior to running

from os import getcwd, listdir
import subprocess

wd = getcwd()
path = wd + "\input\\"
    
input_file_list = listdir(path)

#The output file by default will be the first file alphabetically + output
first_file_name,ext = sorted(input_file_list)[0].split('.')
output_file = path + first_file_name + '_output.' + ext

#Create an external input file
external_file = 'input_file.txt'
with open(external_file,'w') as file_object:
    for i in input_file_list:
        file_object.write('file ' + '\'' + path + i + '\'' + '\n')

cmd = 'ffmpeg -y -f concat -safe 0 -i %s -c copy %s' %(external_file,output_file)
subprocess.call(cmd,shell=True)