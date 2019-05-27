# -*- encoding: utf-8 -*- 
''' 
@File : tickets.py 
@Description: None
@Contact : 17210180033@fudan.edu.cn
@Created info: Yangsj 2019-05-26 22:52
''' 
import requests
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import time
import logging
from bs4 import BeautifulSoup as bs
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def log_info(flag):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('wacth_log.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info(flag)
    logger.removeHandler(handler)
    return logger

def send_mail(flag,sender='yangsjfdu@163.com',receiver='yangsjfdu@163.com'):
    mail_host = 'smtp.163.com'
    mail_user = 'yangsjfdu@163.com'
    mail_pass = 'lj363700'

    now=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    message=MIMEText(now+'：有'+flag+'的余票','plain','utf-8')
    message['From'] = sender
    message['To'] = receiver
    subject = '荷兰梵高博物馆余票监控'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receiver, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")
    except smtplib.SMTPException as error:
        print(error)

def watching(targetdays):
    url='https://tickets.vangoghmuseum.com/zh/purchase-your-tickets-in-chinese?_ga=2.173479651.1332556504.1558901259-887480865.1558599595 '
    s = requests.get(url, verify=False)
    soup=bs(s.content,"lxml")
    vars=soup.find(type="text/javascript").text
    soldoutdays=re.findall(r"(\d{4}-\d{1,2}-\d{1,2})",vars)

    for i in targetdays:
        if i not in soldoutdays:
            return i
def main():
    flag=False
    while(not flag):
        flag=watching(['2019-05-30', '2019-05-31'])
        log_info(time.strftime('%Y-%m-%d %H:%M:%S: ',time.localtime(time.time()))+'当前无余票')
        time.sleep(30)
    print('发现余票！！！')
    send_mail(flag)

if __name__ == '__main__':
    main()