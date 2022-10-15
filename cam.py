#!/usr/bin/python3
import os
os.system('ls ./shot | grep .jpg  > ./shot/list.txt')  # List of jpeg files
a=open('./shot/list.txt')
b=a.read()
c=b.split() # Split to file one by one
print(c)
l=len(c) # Who last
print(l)
os.system(f'fswebcam -r 640x480 --jpeg 85 -D 1 /home/lubuntu/to_test/Cam/shot/{l}.jpg  >> log_shot.txt 2>&1')
os.system('date >> log_shot.txt')
a.close()

