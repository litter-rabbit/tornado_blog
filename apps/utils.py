from email.mime.text import MIMEText
import smtplib

from setting import smtp_server, email_admin, email_password
from email.utils import parseaddr, formataddr
from email.header import Header


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def sned_email(content, email):
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr('来自 <%s>' % email_admin)
    msg['To'] = _format_addr('管理员 <%s>' % email)
    msg['Subject'] = Header('来自小兔子', 'utf-8').encode()
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(1)
    server.login(email_admin, email_password)
    server.sendmail(email_admin, [email], msg.as_string())
    server.quit()


if __name__ == '__main__':
    sned_email('测试', '709343607@qq.com')
