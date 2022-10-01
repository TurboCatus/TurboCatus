#! /usr/bin/python3
a=open('arp_ip.txt')
b=a.read()
c=b.split()
o=[i for i in b]
o.pop()
o.pop(0)
addr=open('ip.txt','w')
for j in o:
  f=j[1:]+j[:10]
  print(f,end='',file=addr)
a.close()
addr.close() 

