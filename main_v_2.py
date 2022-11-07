from netmiko import ConnectHandler
import os
import telebot
import time

# Блок поиска vlan и mac адреса на коммутаторе и вышрузка в файл arp.txt
port=input('Eneter number port for scan:')
#port = ('1/0/22','3/0/4','3/0/7')  # Номер порта коммутатора с которого нужен ip-адрес
port_scan = ('1/0/15')  # Номер порта к которому подключен сканер(ноутбук)
arp = open('arp.txt','w')
switch = {'device_type': 'cisco_ios', 'ip': '192.168.3.135', 'username': 'root', 'password': 'root12345',
          'secret': 'root12345'}
connect = ConnectHandler(**switch)
#connect.enable()
#print(connect.find_prompt())
output = connect.send_command(f'show mac-addr-table interface {port}') #команда на коммутаторе Qtech
#connect.disconnect()
print(output)
print(output,file=arp)
arp.close()
# Блок разделение по файлам mac-адрес в файл MAC.txt, VLAN в файл Vlan.txt
mac_add=open('arp.txt')
MAC=open('MAC.txt','w')
Vlan=open('Vlan.txt','w')
Mac=mac_add.read()
a=Mac.split() #Разделяем на слова
#print(a)
print(a[9],file=Vlan) #позиция номера vlan в файле и запись в Vlan.txt
# Цикл подготовки mac для поиска в WIN
for q in a[8::3]:
    r=q.replace(':','-')# замена : на тире
    low=r.lower()# переход на нижний регистр
    print(low,file=MAC)
MAC.close()

#Блок для вывода готовых mac адресов (Нужен ли?)
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
Vlan.close()
print('End scan.')
# Блок вывода ip-адреса
Raw_ip=open('RAW_IP.txt')
ip_fin=open('IP.txt','w')
ip=Raw_ip.read()
ip_a=ip.split()
IP_FIN=[] # Добавление в список ip адресов
for j in range(len(ip_a)):
    if j%4==0:
        IP_FIN.append(ip_a[j]) # Добавляет только значения кратные 4
print(IP_FIN,file=ip_fin) #Запись ip адреса в файл.
print(IP_FIN) #Вывод ip-адресов
Raw_ip.close()
ip_fin.close()
#for k in IP_FIN:
# os.system(f'cd "C:\\Program Files (x86)\\Nmap" | nmap -O {k} > OS.txt')
os.system('del C:\\Users\\SmychkovSA\\PycharmProjects\\pythonProject1\\RAW_IP.txt')
os.system('copy C:\\Users\\SmychkovSA\\PycharmProjects\\pythonProject1\\IP.txt old_IP.txt')
os.system('del C:\\Users\\SmychkovSA\\PycharmProjects\\pythonProject1\\IP.txt')

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
token = '5629862008:AAGbPMYXqcmthw-vW-tvyoUfdGkQ_Qdl_Gw'
bot = telebot.TeleBot(token)
chat_id = '1366665116'
text = IP_FIN
try:
    for h in IP_FIN:
         bot.send_message(chat_id, h)
         time.sleep(15)
except:
    for h in IP_FIN:
        bot.send_message(chat_id, h)
        time.sleep(25)
print('All Done.')
'''
  import smtpmail
    import os

    sender = os.getenv('smpt_sender')
    pswd = os.getenv('smtp_pass')
    host = os.getenv('smtp_host', 'smtp.gmail.com')
    port = os.getenv('smtp_port', 587)
    read_only_settings: smtpmail.Settings = smatpmail.Mail.init(sender, pswd, host, port)
    ###
    smtpmail.Mail.send_mail(to, subject, content, content_type='plain')
    '''

