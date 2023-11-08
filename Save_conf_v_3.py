from netmiko import ConnectHandler
import time
import os

import datetime
import pathlib
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#--Функция сохранения в файл
def save(data,path):
    with open(path,'a') as f:
        print(data,file=f)
#--Функция сохранения в файл без перезаписи
def add_save(data,path):
    with open(path,'w') as f:
        print(data,file=f)

#--Функция записи конфига в файл
def quantity(add,str_num):
    switch = {'device_type': 'cisco_ios', 'ip': add , 'username': 'root', 'password': 'root',
              'secret': 'root'}
    connect = ConnectHandler(**switch)
    connect.enable()
    # print(connect.find_prompt())
    output1 = connect.send_command('sh run', expect_string='[-#/!Esc@!,.]', delay_factor=100)  #
    i = 0
    print(output1)
    while i != str_num:  # Цикл строк
        output2 = connect.send_command(' ', expect_string='[/!Esc@!,.]') # Читает построчно
        i = i + 1
        print(i, output2)
        save(output2, 'conf.txt')
    time.sleep(5)
    with open('conf.txt') as file:
        pure = [q for q in file if not q == '\x1b[0mMore: <space>,  Quit: q or CTRL+Z, One line: <return> \n'] # Удаляет строку из файла
        fin = '\n'.join(pure)
        save(fin, f'C:\\Users\\username\\PycharmProjects\\Conf_network_main\\conf\\ip_addr_{add}.txt') # Сохранение в файл
        #print(fin)
        file.close()
        os.system('del C:\\Users\\username\\PycharmProjects\\Conf_network_main\\conf.txt') # Удаляет файл conf.txt
        time.sleep(10)
    connect.disconnect()


#--Для проставление даты
x = datetime.datetime.now()
add_save(x,'log.txt')
#print(x.day, x.month, x.year,sep='|')

#--Блок доступа к коммутатору
lst_cisco=[137,139,140]
lst_qtech=[130,131,135,136,138]

#--Конфигурация Qtech
try:
    for j in lst_qtech:
        switch = {'device_type': 'cisco_ios', 'ip': f'192.168.3.{j}', 'username': 'root', 'password': 'root',
                  'secret': 'root'}
        connect = ConnectHandler(**switch)
        connect.enable()
        output = connect.send_command('show running-config')
        save(output,f'C:\\Users\\username\\PycharmProjects\\Conf_network_main\\conf\\ip_addr_192_168_3_{j}.txt')
        #print(output)
        time.sleep(5)
        connect.disconnect()
    add_save('Collect config Qtech finished.','log.txt')
    print('Collect config Qtech finished.')
except:
    add_save('Check save in Qtech section.', 'log.txt')
    print('Check save in Qtech section.')

#--Конфигурация Cisco
try:
    for k in lst_cisco:
        if k==lst_cisco[0]:
            quantity(f'192.168.3.{lst_cisco[0]}', 302)
        if k==lst_cisco[1]:
            quantity(f'192.168.3.{lst_cisco[1]}', 84)
        if k==lst_cisco[2]:
            quantity(f'192.168.3.{lst_cisco[2]}', 249)
    add_save('Collect config Cisco finished.', 'log.txt')
    print('Collect config Cisco finished.')
except:
    add_save('Check save in Cisco section.', 'log.txt')
    print('Check save in Cisco section.')

#--Добавление в архив
try:
    directory = pathlib.Path("C:\\Users\\username\\PycharmProjects\\Conf_network_main\\conf")
    with zipfile.ZipFile(f'{x.day}_{x.month}_{x.year}_config.zip', mode="w") as archive:
        for file_path in directory.iterdir():
            archive.write(file_path, arcname=file_path.name)
    add_save('Zip_file done.', 'log.txt')
    print('Zip_file done.')
except:
    add_save('Check zip section.', 'log.txt')
    print('Check zip section.')

#--Отправка на почту
try:
    mail_content = 'Weekly config'# Message to send in body
#--The mail addresses and password
    sender_address = 'mail'
    sender_pass = 'pass'
    receiver_address = 'mail'

#--Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = f'{x.day}_{x.month}_{x.year}_config'   #The subject line
#--The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))

#--The body and the attachments for the mail
    attach_file_name = f'{x.day}_{x.month}_{x.year}_config.zip'
    attach_file = open(attach_file_name,'rb')
    payload = MIMEBase('application','octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    attach_file.close()
    message.attach(payload)

#--Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    add_save('Email send.', 'log.txt')
    print('Email send.')
except:
    add_save('Check email sender.', 'log.txt')
    print('Check email sender.')

#--Очистка файлов
lst_cisco_rm=[137,139,140]
lst_qtech_rm=[130,131,135,136,138]
try:
#--Удаление файлов конфигурации Qtech
    for rem in lst_qtech_rm:
        os.system(f'del C:\\Users\\username\\PycharmProjects\\Conf_network_main\\conf\\ip_addr_192_168_3_{rem}.txt ')
    add_save('File Qtech deleted.', 'log.txt')
    print('File Qtech deleted.')
except:
    add_save('Check delete file from Qtech', 'log.txt')
    print('Check delete file from Qtech')

#--Удаление файлов конфигурации Cisco
try:
    for rem in lst_cisco_rm:
        os.system(f'del C:\\Users\\username\\PycharmProjects\\Conf_network_main\\conf\\ip_addr_192.168.3.{rem}.txt ')
    add_save('File Cisco deleted.', 'log.txt')
    print('File Cisco deleted.')
except:
    add_save('Check delete file from Cisco', 'log.txt')
    print('Check delete file from Cisco')

#--Отсечка даты
add_save('-------------------------------','log.txt')
