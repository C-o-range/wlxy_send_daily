# -*- coding:utf-8 -*-
# @FileName  :物流学院文件推送.py
# @Time      :2022-09-26 14:44
# @Author    :C_Orange
import os
import re
import warnings
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

import requests
from requests.packages import urllib3

# 关闭ssl警告
urllib3.disable_warnings()
warnings.filterwarnings("ignore")


def open_journal():
    j = open('./journal.txt', 'r', encoding='utf-8')
    info_ = []  # {0: '关于“百蝶杯”第八届全国大学生物流仿真设计大赛校内选拔和统一报名的通知', 1: '物流学院2022-2023学年第1学期的教材选用与审核结果公示', 2: '物流学院关于推荐“2022年本科教育教学研究与改革项目暨本科教学工程项目”申报项目公示二', 3: '物流学院关于推荐“2022年本科教育教学研究与改革项目暨本科教学工程项目”申报项目公示', 4: '物流学院第四届“最受学生欢迎教师”奖第一阶段投票结束入围教师公示', 5: '关于 “百蝶杯”第七届全国大学生物流仿真设计大赛校内选拔的通知'}
    lines = j.readlines(500)
    j.close()
    for i in range(len(lines)):
        line = lines[i].strip('\n[]').split(', ')[1][1:-1]
        info_.append(line)
    return info_


# 参数是收件人
def sendQQ(receivers):
    msg = MIMEText(email_text, 'plain', 'utf-8')
    msg['From'] = formataddr((sendName, login_sender))
    # 邮件的标题
    msg['Subject'] = title
    try:
        # 服务器
        server = smtplib.SMTP_SSL(mail_host, int(mail_port))
        server.login(login_sender, login_pass)
        server.sendmail(login_sender, [receivers, ], msg.as_string())
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
notice_list = open_journal()  # ['关于“百蝶杯”第八届全国大学生物流仿真设计大赛校内选拔和统一报名的通知', '物流...]

try:
    send_new_url = ''
    send_new_tittle = ''
    for i in range(3):
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

            mail_port = '465'  # Linux平台上面发

            # 发件人邮箱账号
            login_sender = '3125178611@qq.com'
            # 发件人邮箱授权码而不是邮箱密码，授权码由邮箱官网可设置生成
            login_pass = 'tavkjnifvjoodgch'
            # 发送者
            sendName = "C_Orange <calhe@qq.com>"
            # 接收者
            # resName = "❤GIN🌙<2487811390@qq.com>;"

            for mail_id in ['2487811390', '3125178611']:
                sendQQ(f'{mail_id}@qq.com')
            """---------------------------------------------------------------------------------------------------------------"""
            with open('./journal.txt', 'r', encoding='utf-8') as f,\
                    open('./new_journal.txt', 'w', encoding='utf-8') as f2:
                old_text = f.read()
                new_text = str([notice_url, ntittle])
                f2.write(new_text + '\n' + old_text)
            # QQ邮箱POP3/SMTP授权码：uqheypmonsbsdchd
            # QQ邮箱IMAP/SMTP授权码：tavkjnifvjoodgch
            os.remove('./journal.txt')
            os.rename('./new_journal.txt', './journal.txt')

except FileNotFoundError as e:
    print(e)

