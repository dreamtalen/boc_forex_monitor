# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')


def main():
    with open("log.txt", "r") as f:
        lines_list = f.readlines() 
    for index, line in enumerate(lines_list):
        if '美元' in line and index > 100:
            old_US_sold_price = float(lines_list[index + 3])
    url = "http://www.boc.cn/sourcedb/whpj/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    with open("log.txt", 'w') as f:
        f.write(soup.text)
    with open("log.txt", "r") as f:
        lines_list = f.readlines() 
        for index, line in enumerate(lines_list):
            if '美元' in line and index > 100:
                US_sold_price = float(lines_list[index + 3])
    print old_US_sold_price, US_sold_price
    if abs(US_sold_price - old_US_sold_price) > 0.001:
        print "PRICE CHANGED"
        send_email(US_sold_price)

def send_email(US_sold_price):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    mail_host="smtp.sina.com"
    mail_user="python_dmtalen@sina.com"
    mail_pass="dmt123456"

    #this one is also username too.
    sender = 'python_dmtalen@sina.com'
    receivers = ['771067560@qq.com']


    message = MIMEText(str(US_sold_price), 'plain', 'utf-8')
    #this on also must be the sender's address
    message['From'] = "python_dmtalen@sina.com"
    message['To'] =  "771067560@qq.com"  #receiver's name could be customized

    subject = 'BOC US SOLD PRICE' #title
    message['Subject'] = Header(subject, 'utf-8')


    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "Success"
    except smtplib.SMTPException as e:
        print "Error: cannot send my email"
        print e

if __name__ == '__main__':
    main()
