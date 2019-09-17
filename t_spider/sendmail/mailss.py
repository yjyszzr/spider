import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formatdate
import os
import time
import datetime


s = time.strftime('%Y-%m')
d = time.strftime('%d')
today = datetime.date.today()
day = datetime.timedelta(days=1)
dat = str(today-day)


#设置登录及服务器信息
mail_host = 'smtp.exmail.qq.com'
mail_user = 'jixiang@caixiaomi.com'
mail_pass = 'Jx0311'
sender = 'jixiang@caixiaomi.com'
to_reciver= ['jixiang@caixiaomi.com']
# cc_reciver = ['guoyanjing@caixiaomi.com','duanyupeng@caixiaomi.com']
receivers = to_reciver
#设置eamil信息
#添加一个MIMEmultipart类，处理正文及附件
message = MIMEMultipart()
message['From'] = sender
message['To'] = receivers[0]
message['Subject'] = '{} iphone日志'.format(dat)
message['Date'] = formatdate( )

thebody = MIMEText('您好:\n附件内容为昨日iphone日志 请查阅', 'plain', 'utf-8')
message.attach(thebody)
#推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等

# with open('abc.html','r') as f:
#     content = f.read()
# #设置html格式参数
# part1 = MIMEText(content,'html','utf-8')
#
# basename = os.path.basename("report.txt")
# #添加一个txt文本附件
# with open('report.txt','r')as h:
#     content2 = h.read()
# #设置txt参数
# part2 = MIMEText(content2,'plain','utf-8')
#
# #附件设置内容类型，方便起见，设置为二进制流
# part2['Content-Type'] = 'application/octet-stream'
# #设置附件头，添加文件名
# part2['Content-Disposition'] = 'attachment;filename=%s' % basename

#解决中文附件名乱码问题
# part2.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', basename))

#添加照片附件
# with open('/Users/admin/Downloads/iphone-{}.csv'.format(dat),'rb')as fp:
#     picture = MIMEImage(fp.read())
#     #与txt文件设置相似
#     picture['Content-Type'] = 'application/octet-stream'
#     picture['Content-Disposition'] = 'attachment;filename="iphone-{}.csv"'.format(dat)


with open('/Users/admin/Downloads/iphone-{}.csv'.format(dat),'rb')as fp:
    picture = MIMEText(fp.read(),'csv','gbk')
    #与txt文件设置相似
    picture['Content-Type'] = 'application/octet-stream'
    picture['Content-Disposition'] = 'attachment;filename="iphone-{}.csv"'.format(dat)
#将内容附加到邮件主体中
# message.attach(part1)
# message.attach(part2)
message.attach(picture)

#登录并发送
try:
    # smtpObj = smtplib.SMTP()
    # smtpObj.connect(mail_host,25)
    #需要SSL认证
    smtpObj = smtplib.SMTP_SSL(mail_host)

    smtpObj.login(mail_user,mail_pass)
    smtpObj.sendmail(sender,receivers,message.as_string())
    print('success')
    smtpObj.quit()
except smtplib.SMTPException as e:
    print('error',e)