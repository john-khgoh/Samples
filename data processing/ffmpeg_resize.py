#Script to resize video files in the specified directory using FFMPEG
#Requires FFMPEG to be installed and added to path prior to running

from os import listdir, remove
import subprocess

path = 'D:\\VIDEO\\'
size = 1920 #FFMPEG automatically ensures the aspect ratio
filename_ext = '_' + str(size)

file_list = listdir(path)

#Iterating through all the file at the specified path and resizing the video
#Deletes the original file once complete
for file in file_list:
    first_file_name,ext = file.split('.')
    input_file_name = path + file
    output_file_name = path + first_file_name + filename_ext + '.' + ext
    cmd = 'ffmpeg -y -i %s -vf scale=%s:-1 %s' %(input_file_name,size,output_file_name)
    subprocess.call(cmd,shell=True)
    remove(input_file_name) #Removing original file
