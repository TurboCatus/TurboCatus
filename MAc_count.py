from netmiko import ConnectHandler
import time
switch={'device_type':'cisco_ios','ip':'192.168.3.130','username':'root','password':'root12345'}
connect=ConnectHandler(**switch)
for j in range(101,107):
  file=open(f'ARP{j}.txt','w')
  output=connect.send_command(f'show mac-addr-table vlan {j}')
  print(output,file=file)
  file.close()
for i in range(101,107): #Счетчик mac адресов
    file_arp=open(f'ARP{i}.txt')
    file_arp_count=open(f'Arp_count{i}.txt','w')
    file_count=open(f'Vlan_{i}_count.txt','w')
    k = 0
    for l in file_arp:#Считает строчки
      k=k+1
      print(l,k,'|',end='',file=file_arp_count)
    k = k - 5 # Минус первые и последние строки, и Managment mac
    print(file=file_arp_count)
    print("Dev mac:", k,file=file_arp_count)
    #print('Dev_mac:',k,'--','Vlan:',i,file=file_count)
    print('Dev_mac:',k,'--','Vlan:',i)
    if i==101:
        print(f'Vlan_{i},free ip:',60-k,file=file_count)
    if i==102:
        print(f'Vlan_{i},free ip:',60-k,file=file_count)
    if i==103:
        print(f'Vlan_{i},free ip:', 28 - k,file=file_count)
    if i==104:
        print(f'Vlan_{i},free ip:', 64 - k,file=file_count)
    if i==105:
        print(f'Vlan_{i},free ip:', 28 - k,file=file_count)
    if i==106:
        print(f'Vlan_{i},free ip:', 28 - k,file=file_count)
    time.sleep(5)
    file_arp.close()
    file_arp_count.close()
    file_count.close()

