#! /usr/bin/python3
import os
os.system ('arp -a > arp.txt')
c='60:ab:67:c2:3e:52'
i=0
with open('arp.txt') as file:
  for line in file:
    i=i+1
    if c in line:
      a=line.split()
      b=a[1]
#print(a)
c=open('arp_ip.txt','w')
print(b,end='',file=c)
c.close()

