from netmiko import ConnectHandler
import time
import os
#Функция сохранения в файл
def save(data,path):
    with open(path,'a') as f:
        print(data,file=f)
#Функция записи конфига в файл
def quantity(add,str_num):
    switch = {'device_type': 'cisco_ios', 'ip': add , 'username': 'root', 'password': 'root12345',
              'secret': 'root12345'}
    connect = ConnectHandler(**switch)
    # connect.enable()
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
        save(fin, f'ip_addr_{add}.txt') # Сохранение в файл
        print(fin)
        file.close()
        os.system('del C:\\Users\\SmychkovSA\\PycharmProjects\\Conf_network_main\\conf.txt') # Удаляет файл conf.txt
        time.sleep(10)
    connect.disconnect()


#--Блок доступа к коммутатору
lst_cisco=[137,139,140]
lst_qtech=[130,131,135,136,138]

for j in lst_qtech:
    switch = {'device_type': 'cisco_ios', 'ip': f'192.168.3.{j}', 'username': 'root', 'password': 'root12345',
                  'secret': 'root12345'}
    connect = ConnectHandler(**switch)
    connect.enable()
    output = connect.send_command('show running-config')
    save(output,f'ip_addr_192_168_3_{j}.txt')
    print(output)
    time.sleep(5)
    connect.disconnect()

for k in lst_cisco:
    if k==lst_cisco[0]:
        quantity(f'192.168.3.{lst_cisco[0]}', 302) #
    if k==lst_cisco[1]:
        quantity(f'192.168.3.{lst_cisco[1]}', 84)
    if k==lst_cisco[2]:
        quantity(f'192.168.3.{lst_cisco[2]}', 249)
print('Collect finish')

