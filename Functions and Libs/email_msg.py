import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import datetime

## 

def emailMessage(to, gmailUsr, gmailPwd, subject, content):

	smtpserver = smtplib.SMTP('smtp.gmail.com',587 )
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmailUsr, gmailPwd)

	'''
	sendDate = datetime.date.today()
	arg = 'ip route list'
	p = subprocess.Popen(arg, shell = True, stdout = subprocess.PIPE)
	data = p.communicate()
	split_data = data[0].split()
	ipaddr = split_data[split_data.index('src')+1]
	my_ip = 'Your ip is %s'% ipaddr
	'''

	msg = MIMEText(content)
	msg['Subject'] = subject #% sendDate.strftime('%l:%M:%S%p %Z on %b %d, %Y')
	msg['From'] = gmailUsr
	msg['To'] = to

	smtpserver.sendmail(gmailUsr, [to], msg.as_string())
	smtpserver.quit()

def email_information(file):
	f = open(file,"r")

	for full_line in f:
		line = full_line.split("\n")
		if "to_email" in line[0]:
			temp_to = line[0].split("=")
			to_email = temp_to[1]

		elif "from_email" in line[0]:
			temp_from = line[0].split("=")
			from_email = temp_from[1]

		elif "pwd_email" in line[0]:
			temp_pwd = line[0].split("=")
			pwd_email = temp_pwd[1]

		elif "title" in line[0]:
			temp_title = line[0].split("=")
			title = temp_title[1]

		elif "sheet" in line[0]:
			temp_sheet = line[0].split("=")
			sheet = temp_sheet[1]

	return to_email, from_email, pwd_email, title, sheet


if __name__ == '__main__':
	emailMessage("galanc3.3@gmail.com","galanc3.3@gmail.com","Vivaldi3","Test","This is a test\n to undertand how email work\t thank you")