from netmiko import ConnectHandler
import os
#1---Поиск vlan и mac адреса на коммутаторе и вышрузка в файл arp.txt
port=('1/0/14') #Номер порта коммутатора
arp=open('arp.txt','w')
switch = {'device_type': 'cisco_ios', 'ip': '192.168.3.135', 'username': 'root', 'password': 'root12345',
          'secret': 'root12345'}
connect = ConnectHandler(**switch)
#connect.enable()
#print(connect.find_prompt())
output = connect.send_command(f'show mac-addr-table interface {port}') #команда на коммутаторе Qtech
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
print(a[8],file=MAC) #позиция mac-адреса в файле(могут быть 2 mac-адреса),8 поз==1 MAC|11 поз==2 MAC
ch=a[8].replace(':','-') #замена с двоеточия на тире(заменить на позицию MAC-адреса)
c=ch.lower() #замена на нижний регистр
print(c)
#3---Сканирование адресов в зависимости от номера Vlan.(Дописать автоматическое переключения vlan на коммутаторе )
if a[9]=='102':
    os.system('cd "C:\\Program Files (x86)\\Nmap" | nmap -F 192.168.1.66-126 > arp_nmap.txt' )
    os.system(f'arp -a | findstr {c} > RAW_IP.txt')
else:
    print('Check VLAN')
#elif a[9]=='101'
#arp -a | findstr 08-8f-c3-09-0e-a1
mac_add.close()
MAC.close()
Vlan.close()
#4---Вывод ip-адреса
Raw_ip=open('Raw_IP.txt')
ip_fin=open('IP.txt','w')
ip=Raw_ip.read()
ip_a=ip.split()
print(ip_a[0],file=ip_fin) #Позиция ip адреса в файле и запись в файл ip_fin.txt
print(ip_a[0])
Raw_ip.close()
ip_fin.close()
os.system(f'cd "C:\\Program Files (x86)\\Nmap" | nmap -O {ip_a[0]} > OS.txt')
