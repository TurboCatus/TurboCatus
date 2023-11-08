'''
# Import Module
import ftplib

# Fill Required Information
HOSTNAME = "ftp.dlptest.com"
USERNAME = "dlpuser@dlptest.com"
PASSWORD = "eUj8GeW55SvYaswqUyDSm5v6N"

# Connect FTP Server
ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

# force UTF-8 encoding
ftp_server.encoding = "utf-8"

# Enter File Name with Extension
filename = "gfg.txt"

# Write file in binary mode
with open(filename, "wb") as file:
	# Command for Downloading the file "RETR filename"
	ftp_server.retrbinary(f"RETR {filename}", file.write)

# Get list of files
ftp_server.dir()

# Display the content of downloaded file
file= open(filename, "r")
print('File Content:', file.read())

# Close the Connection
ftp_server.quit()
'''
import time

'''
# Import Module
import ftplib

# Fill Required Information
HOSTNAME = ""
USERNAME = ""
PASSWORD = ""

# Connect FTP Server
ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

# force UTF-8 encoding
ftp_server.encoding = "utf-8"

# Enter File Name with Extension
filename = "main_v_2.py"

# Read file in binary mode
with open(filename, "rb") as file:
	# Command for Uploading the file "STOR filename"
	ftp_server.storbinary(f"STOR {filename}", file)

# Get list of files
ftp_server.dir()

# Close the Connection
ftp_server.quit()
'''

'''
import smtplib
s=smtplib.SMTP('smtp.gmail.com',587)
s.starttls()
s.login('stas.smy@gmail.com','fmuhuhtnmljigsuj')
message = 'Some message'
s.sendmail('stas.smy@gmail.com','stas.smy@gmail.com',message)
s.quit()
'''


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
mail_content = 'Another test for send massage'#Message to send in body
#The mail addresses and password
sender_address = 'stas.smy@gmail.com'
sender_pass = 'fmuhuhtnmljigsuj'
receiver_address = 'stas.smy@gmail.com'

#Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line
#The body and the attachments for the mail
message.attach(MIMEText(mail_content, 'plain'))

#The body and the attachments for the mail
attach_file_name = 'keks.rar'
attach_file = open(attach_file_name,'rb')
payload = MIMEBase('application','octate-stream')
payload.set_payload((attach_file).read())
encoders.encode_base64(payload)
payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
attach_file.close()
message.attach(payload)

#Create SMTP session for sending the mail
session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
session.starttls() #enable security
session.login(sender_address, sender_pass) #login with mail_id and password
text = message.as_string()
session.sendmail(sender_address, receiver_address, text)
session.quit()

#print(time.localtime())
