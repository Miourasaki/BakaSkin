import base64
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 邮件服务器的地址
mail_host = "smtp.qq.com"
# 发件人邮箱
# 收件人邮箱
# 发件人邮箱登录账号
mail_username = "ba13k@foxmail.com"
# 发件人邮箱登录密码
mail_password = "dzlukqytzidobehi"


def send_email(code: str, to: str, mail_receiver: str, putURL: bool = False) -> bool:
    html_content = f"""
    <html>
    <body>
    <p>You Code: {code}</p>
    <p>Check <a href="https://baka.skin/api/verify?code={code}">here</a> to verify。</p>
    <p>or copy link to you browser:</p>
    <p>https://baka.skin/api/verify?code={code}</p>
    </body>
    </html>
    """

    # 邮件内容
    message = MIMEText(html_content, 'html')
    if not putURL:
        message = MIMEText(f'You code: {code}', 'plain', 'utf-8')
    message['From'] = f"Baka Cirno <{mail_username}>"
    message['To'] = Header(to, 'utf-8')
    message['Subject'] = Header('BakaRealm SMTP Server', 'utf-8')

    # 发送邮件
    try:
        smtp_obj = smtplib.SMTP_SSL(mail_host, 465)
        smtp_obj.login(mail_username, mail_password)
        smtp_obj.sendmail(mail_username, mail_receiver, message.as_string())
        return True
    except smtplib.SMTPException as e:
        return False


def send_password(code: str, to: str, mail_receiver: str) -> bool:
    html_content = f"""
    <html>
    <body>
    <p>You new password: {code}</p>
    <p>Check <a href="https://baka.skin/login">here</a> to login。</p>
    <p>Please set a new password as soon as possible</p>
    </body>
    </html>
    """

    # 邮件内容
    message = MIMEText(html_content, 'html')
    message['From'] = f"Baka Cirno <{mail_username}>"
    message['To'] = Header(to, 'utf-8')
    message['Subject'] = Header('BakaRealm SMTP Server', 'utf-8')

    # 发送邮件
    try:
        smtp_obj = smtplib.SMTP_SSL(mail_host, 465)
        smtp_obj.login(mail_username, mail_password)
        smtp_obj.sendmail(mail_username, mail_receiver, message.as_string())
        return True
    except smtplib.SMTPException as e:
        return False

