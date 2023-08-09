#Script to resize video files in the specified directory using FFMPEG
#Requires FFMPEG to be installed and added to path prior to running

from os import getcwd,listdir, remove
import subprocess

path = 'D:\\VIDEO\\'
size = 2160 #FFMPEG automatically ensures the aspect ratio
fps = 10
filename_ext = '_' + str(size)

file_list = listdir(path)

#Iterating through all the file at the specified path and resizing the video
#Deletes the original file once complete
for file in file_list:
    first_file_name,ext = file.split('.')
    input_file_name = path + file
    intermediate_file_name = path + first_file_name + '_' + '.' + ext
    output_file_name = path + first_file_name + filename_ext + '.' + ext
    #Changing the frame rate
    cmd1 = 'ffmpeg -y -i %s -filter:v fps=%s %s' %(input_file_name,fps,intermediate_file_name)
    subprocess.call(cmd1,shell=True)
    #Removing original file
    remove(input_file_name)
    #Rescaling the video
    cmd2 = 'ffmpeg -y -i %s -vf scale=%s:-1 %s' %(intermediate_file_name,size,output_file_name)
    subprocess.call(cmd2,shell=True)
    #Removing the intermediate file
    remove(intermediate_file_name) 
    
