from netmiko import ConnectHandler
import time
import telebot #pyTelegrammbotApi
#import  pywhatkit
#--Блок отправки в телеграмм
token = '5629862008:AAGbPMYXqcmthw-vW-tvyoUfdGkQ_Qdl_Gw'
bot = telebot.TeleBot(token)
chat_id = '1366665116'
#--Блок доступа к коммутатору
switch={'device_type':'cisco_ios','ip':'192.168.3.130','username':'root','password':'root12345'}
connect=ConnectHandler(**switch)
# Блок создает файлы с номером Vlan и записывает mac адреса для данного Vlan
for j in range(101,107):
  file=open(f'ARP{j}.txt','w')
  output=connect.send_command(f'show mac-addr-table vlan {j}')
  print(output,file=file)
  file.close()
# Блок счетчик
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
    # Считает разность между количеством ip адресов в пуле и сущ. mac адресами
    if i==101:
        print(f'Vlan_{i},free ip:',60-k,file=file_count)
        print(f'Vlan_{i},free ip:', 60 - k)
        if (60-k) < 3:
            text = f'Warning, vlan {i}, has no free ip addreses!'
            try:
                bot.send_message(chat_id, text)
                time.sleep(15)
            except:
                bot.send_message(chat_id, text)
                time.sleep(25)
    if i==102:
        print(f'Vlan_{i},free ip:',60-k,file=file_count)
        print(f'Vlan_{i},free ip:', 60 - k)
        if (60-k) < 3:
            text = f'Warning, vlan {i}, has no free ip addreses!'
            try:
                bot.send_message(chat_id, text)
                time.sleep(15)
            except:
                bot.send_message(chat_id, text)
                time.sleep(25)
    if i==103:
        print(f'Vlan_{i},free ip:', 28 - k,file=file_count)
        print(f'Vlan_{i},free ip:', 28 - k)
        if (28-k) < 3:
            text = f'Warning, vlan {i}, has no free ip addreses!'
            try:
                bot.send_message(chat_id, text)
                time.sleep(15)
            except:
                bot.send_message(chat_id, text)
                time.sleep(25)
    if i==104:
        print(f'Vlan_{i},free ip:', 64 - k,file=file_count)
        print(f'Vlan_{i},free ip:', 64 - k)
        if (64-k) < 3:
            text = f'Warning, vlan {i}, has no free ip addreses!'
            try:
                bot.send_message(chat_id, text)
                time.sleep(15)
            except:
                bot.send_message(chat_id, text)
                time.sleep(25)
    if i==105:
        print(f'Vlan_{i},free ip:', 28 - k,file=file_count)
        print(f'Vlan_{i},free ip:', 28 - k)
        if (28-k) < 3:
            text = f'Warning, vlan {i}, has no free ip addreses!'
            try:
                bot.send_message(chat_id, text)
                time.sleep(15)
            except:
                bot.send_message(chat_id, text)
                time.sleep(25)
    if i==106:
        print(f'Vlan_{i},free ip:', 28 - k,file=file_count)
        print(f'Vlan_{i},free ip:', 28 - k)
        if (28-k) < 2:
            text = f'Warning, vlan {i}, has no free ip addreses!'
            try:
                bot.send_message(chat_id, text)
                time.sleep(15)
            except:
                bot.send_message(chat_id, text)
                time.sleep(25)
    time.sleep(5)
    file_arp.close()
    file_arp_count.close()
    file_count.close()
#pywhatkit.sendwhatmsg('+79234228095', 'Тест',15,52)
print('Finish scan.')

