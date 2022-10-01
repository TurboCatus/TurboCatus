#! /usr/bin/python3
import os
add='192.168.1.4'
p=os.system('ping -c 3 %s > ping.txt'%(add)) #ping ip address
#log=os.system('touch log_sync.txt')
a=open('ping.txt')
b=a.read()
c=('time=') #if ping done
p=('8022/tcp') # key word for test port
# ss=os.system('nmap 192.168.1.3 > test_ssh.txt')
port=os.system('nmap %s > port.txt'%(add)) # test port
pp=open('port.txt')
ppp=pp.read()
if p in ppp:
  os.system('date >> log_sync.txt|echo port_open >> log_sync.txt')
else:
  os.system('echo port_not_open_or_not_present >> log_sync.txt')
if c not in a:
  os.system('echo host_not_reachable >> log_sync.txt|date >> log_sync.txt|echo ----- >> log_sync.txt') #test ping
#if p not in port:
#  os.system('echo port_not_open >> log_sync.txt|date >> log_sync.txt|echo----->> log_sync.txt') #test port
 #проверка на отсутствие ошибок, на пустой файл с ошибками для подключения по ssh
if (c in b) and (p in ppp):
    #os.system('echo all_done >> log_sync.txt|date >> log_sync.txt|echo ----- >> log_sync.txt') # log
    os.system('rsync -avzhe "ssh -p 8022" Linux@%s:/data/data/com.termux/files/home/storage/shared/Android/media/com.whatsapp/WhatsApp/Media/ /media/lubuntu/cecdbebf-1288-4fcc-9e7e-c59f15bf5af8/Phone_back/ >> log_sync.txt'%(add)) #log syncro
    #os.system('rsync -avzhe "ssh -p 8022" Linux@192.168.1.4:/data/data/com.termux/files/home/test/ /media/lubuntu/cecdbebf-1288-4fcc-9e7e-c59f15bf5af8/Phone_back/')
 #отправка отчета на почту
else:
    os.system('echo something_not_ok >> log_sync.txt|date >> log_sync.txt|echo ----- >> log_sync.txt')

