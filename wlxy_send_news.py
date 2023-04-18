# -*- coding:utf-8 -*-
# @FileName  :物流学院文件推送.py
# @Time      :2022-09-26 14:44
# @Author    :C_Orange
import datetime
import os
import re
import warnings
import smtplib
from email.mime.text import MIMEText

import requests
from requests.packages import urllib3

# 关闭ssl警告
urllib3.disable_warnings()
warnings.filterwarnings("ignore")


def open_journal():
    j = open('./journal.txt', 'r', encoding='utf-8')
    info_ = []
    lines = j.readlines(500)
    j.close()
    for i in range(len(lines)):
        line = lines[i].strip('\n[]').split(', ')[1][1:-1]
        info_.append(line)
    return info_


# 参数是收件人
def sendQQ(receivers):
    msg = MIMEText(email_text, 'plain', 'utf-8')
    msg['From'] = login_sender
    # 邮件的标题
    msg['Subject'] = title
    try:
        # 服务器
        server = smtplib.SMTP_SSL(mail_host)
        server.login(login_sender, login_pass)
        server.sendmail(login_sender, receivers, msg.as_string())
        print("已发送到" + receivers + "的邮箱中！")
        server.quit()

    except smtplib.SMTPException:
        print("发送邮箱失败！")


# 爬取内容
url = 'https://wlxy.cuit.edu.cn/xwgg/tzgg.htm'
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 Edg/104.0.1293.70",
}

res = requests.get(url, verify=False)
res.encoding = 'utf-8'
info_list = re.findall('<a class="c1012826" href="(.*?)" target="_blank" title="(.*?)"', res.text)

# 读取日志前五行
notice_list = open_journal()

try:
    send_new_url = ''
    send_new_tittle = ''
    for i in range(2):
        nurl, ntittle = list(info_list[i])
        notice_url = "https://wlxy.cuit.edu.cn" + nurl[2:]
        if ntittle in notice_list:
            pass
        else:
            send_new_url = notice_url
            send_new_tittle = ntittle
            # 邮箱文本内容
            email_text = f"有新比赛啦：\n{send_new_tittle}\n{send_new_url}"
            # 邮箱正文标题
            title = send_new_tittle
            """---------------------------------------------------------------------------------------------------------------"""
            ##### 配置区  #####
            mail_host = 'smtp.qq.com'
            # 发件人邮箱账号
            login_sender = '3125178611@qq.com'
            # 发件人邮箱IMAP/SMTP授权码而不是邮箱密码，授权码由邮箱官网可设置生成
            login_pass = 'dwuvfhbncqtodeeb'

            # 接收者
            resName = ["2487811390", "3125178611"]
            for mail_id in resName:
                sendQQ(f'{mail_id}@qq.com')
            """---------------------------------------------------------------------------------------------------------------"""
            with open('./journal.txt', 'r', encoding='utf-8') as f,\
                    open('./new_journal.txt', 'w', encoding='utf-8') as f2:
                old_text = f.read()
                new_text = str([notice_url, ntittle])
                f2.write(new_text + '\n' + old_text)
            # QQ邮箱IMAP/SMTP授权码：dwuvfhbncqtodeeb
            os.remove('./journal.txt')
            os.rename('./new_journal.txt', './journal.txt')

            with open('./log.txt', 'a+', encoding='utf-8') as f3:
                f3.write(f'{datetime.datetime.now()} 更新-内容：{title} {send_new_url}\n')

except FileNotFoundError as e:
    print(e)

