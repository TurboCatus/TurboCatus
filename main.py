from netmiko import ConnectHandler
import os
'''
#1---Поиск vlan и mac адреса на коммутаторе и вышрузка в файл arp.txt
port=('1/0/15')
arp=open('arp.txt','w')
switch = {'device_type': 'cisco_ios', 'ip': '192.168.3.135', 'username': 'root', 'password': 'root12345',
          'secret': 'root12345'}
connect = ConnectHandler(**switch)
#connect.enable()
#print(connect.find_prompt())
output = connect.send_command(f'show mac-addr-table interface {port}')
print(output)
print(output,file=arp)
arp.close()
#2---Разделение по файлам mac-адрес в файл MAC.txt, VLAN в файл Vlan.txt
mac_add=open('arp.txt')
MAC=open('MAC.txt','w')
Vlan=open('Vlan.txt','w')
Mac=mac_add.read()
a=Mac.split()
#print(a)
print(a[9],file=Vlan) #позиция vlan в файле
print(a[11],file=MAC) #позиция mac-адреса в файле(могут быть 2 mac-адреса)
ch=a[11].replace(':','-') #замена с двоеточия на тире
c=ch.lower() #замена на нижний регистр
#print(c)
#3---Сканирование адресов в зависимости от номера Vlan.(Дописать автоматическое переключения vlan на коммутаторе )
if a[9]=='102':
    os.system('cd "C:\\Program Files (x86)\\Nmap" | nmap -F 192.168.1.66-126 > arp_nmap.txt' )
    os.system(f'arp -a | findstr {c} > RAW_IP.txt')
#elif a[9]=='101'
#arp -a | findstr 08-8f-c3-09-0e-a1
mac_add.close()
MAC.close()
Vlan.close()'''
#4---Вывод ip-адреса
Raw_ip=open('Raw_IP.txt')
ip_fin=open('IP.txt','w')
ip=Raw_ip.read()
ip_a=ip.split()
print(ip_a[0],file=ip_fin)
print(ip_a[0])
Raw_ip.close()
ip_fin.close()

