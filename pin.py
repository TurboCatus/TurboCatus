#!/usr/bin/python3
import os
#a='192.168.1.1'
a=open('ip.txt')
c=a.read()
#print(c)
b=os.system('ping -c 3 %s '%(c))
print(b)
