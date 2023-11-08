from netmiko import ConnectHandler
import os
import telebot
import time

def save(data,path):
    with open(path,'a') as f:
        print(data,file=f)

# Блок поиска vlan и mac адреса на коммутаторе и выгрузка в файл arp.txt
#sw_ip=input('Enter switch ip address:') #Ввод ip адреса коммутатора
port=input('Eneter number port for scan:')
#port = ('1/0/22','3/0/4','3/0/7')  # Номер порта коммутатора с которого нужен ip адрес
port_scan = ('1/0/15')  # Номер порта к которому подключен сканер(ноутбук)

switch = {'device_type': 'cisco_ios', 'ip': '192.168.3.135', 'username': 'admin', 'password': 'admin',
          'secret': 'admin'}
connect = ConnectHandler(**switch)
#connect.enable()
#print(connect.find_prompt())
output = connect.send_command(f'show mac-addr-table interface {port}') #команда на коммутаторе Qtech показать mac адреса
#connect.disconnect()
print(output)
save(output,'arp.txt')

# Блок разделение по файлам mac-адрес в файл MAC.txt, VLAN в файл Vlan.txt
mac_add=open('arp.txt')
Mac=mac_add.read()
a=Mac.split() #Разделяем на слова
save(a[9],'Vlan.txt')
#print(a[9],file=Vlan) #позиция номера vlan в файле и запись в Vlan.txt

# Цикл подготовки mac для поиска в WIN
for q in a[8::3]:
    r=q.replace(':','-')# замена : на тире
    low=r.lower()# переход на нижний регистр
    save(low,'MAC.txt')

#Блок для вывода готовых mac адресов

file=open('MAC.txt')
rd=file.read()
spl=rd.split()
print(spl) # Вывод MAC адресов
time.sleep(5)

# Блок изменения номера Vlan на порту

try:
    #connect = ConnectHandler(**switch)
    connect.enable()
    output_2 = connect.send_config_set([f'interface {port_scan}',f'switchport access vlan {a[9]}'])  # команда на коммутаторе Qtec переключение порта на заданный VLAN
    connect.disconnect()
except:
    pass

# Блок переполучения ip адреса сетевой картой
print('Stage_release.')
os.system('ipconfig /release')
time.sleep(60)
print('Stage_renew')
os.system('ipconfig /renew')
time.sleep(60)

# Блок сканирование адресов в зависимости от номера Vlan.
print('Start scan')
if a[9]=='102':
    os.system('cd "C:\\Program Files (x86)\\Nmap" | nmap -F 192.168.1.66-126 > arp_nmap.txt' )
    for i in spl:
        os.system(f'arp -a | findstr {i} >> RAW_IP.txt')
elif a[9]=='101':
    os.system('cd "C:\\Program Files (x86)\\Nmap" | nmap -F 192.168.1.2-62 > arp_nmap.txt' )
    for i in spl:
        os.system(f'arp -a | findstr {i} >> RAW_IP.txt')
elif a[9]=='103':
    os.system('cd "C:\\Program Files (x86)\\Nmap" | nmap -F 192.168.1.130-158 > arp_nmap.txt' )
    for i in spl:
         os.system(f'arp -a | findstr {i} >> RAW_IP.txt')
elif a[9]=='104':
    os.system('cd "C:\\Program Files (x86)\\Nmap" | nmap -F 192.168.1.162-190 > arp_nmap.txt' )
    for i in spl:
         os.system(f'arp -a | findstr {i} >> RAW_IP.txt')
elif a[9]=='105':
    os.system('cd "C:\\Program Files (x86)\\Nmap" | nmap -F 192.168.1.194-222 > arp_nmap.txt' )
    for i in spl:
        os.system(f'arp -a | findstr {i} >> RAW_IP.txt')
elif a[9]=='106':
    os.system('cd "C:\\Program Files (x86)\\Nmap" | nmap -F 192.168.1.226-254 > arp_nmap.txt' )
    for i in spl:
        os.system(f'arp -a | findstr {i} >> RAW_IP.txt')
else:
    print('Check VLAN.')
mac_add.close()
file.close()
print('End scan.')

# Блок вывода ip-адреса
Raw_ip=open('RAW_IP.txt')
#ip_fin=open('IP.txt','w')
ip=Raw_ip.read()
ip_a=ip.split()
IP_FIN=[] # Добавление в список ip адресов
for j in range(len(ip_a)):
    if j%4==0:
        IP_FIN.append(ip_a[j]) # Добавляет только значения кратные 4
save(IP_FIN,'IP.txt')
#print(IP_FIN,file=ip_fin) #Запись ip адреса в файл.
print(IP_FIN) #Вывод ip-адресов
Raw_ip.close()

#for k in IP_FIN:
# os.system(f'cd "C:\\Program Files (x86)\\Nmap" | nmap -O {k} > OS.txt')


time.sleep(10)

# Блок возвращения порта в начальное состояние (102 Vlan)
try:
    connect = ConnectHandler(**switch)
    connect.enable()
    output_3 = connect.send_config_set([f'interface {port_scan}','switchport access vlan 102'])  # команда на коммутаторе Qtec переключение порта на заданный VLAN
    connect.disconnect()
except:
    pass

# Блок переполучения ip адреса
print('Stage_2_release.')
os.system('ipconfig /release')
time.sleep(60)
print('Stage_2_renew')
os.system('ipconfig /renew')
time.sleep(60)
print('Stage_Send to telegramm.')

# Блок отправки в телеграм
token = 'token'
bot = telebot.TeleBot(token)
chat_id = 'chatid'
text = IP_FIN
try:
    for h in IP_FIN:
         bot.send_message(chat_id, h)
         time.sleep(15)
except:
    for h in IP_FIN:
        bot.send_message(chat_id, h)
        time.sleep(25)

# Блок удаляет за собой старые файлы
os.system('del arp.txt')
os.system('del MAC.txt')
os.system('del Vlan.txt')
os.system('del RAW_IP.txt')
os.system('copy IP.txt old_IP.txt')
os.system('del IP.txt')
print('All Done.')
