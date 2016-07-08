from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText


def sendMail(dest, title, text):
    mailInfo = {
        "from": "JijunHe@qq.com",
        "to": dest,
        "hostname": "smtp.qq.com",
        "username": "JijunHe@qq.com",
        "password": "sjycupiwuhoyecgc",
        "mailsubject": title,
        "mailtext": text,
        "mailencoding": "utf-8"
    }
    try:
        smtp = SMTP_SSL(mailInfo["hostname"])
        smtp.set_debuglevel(1)
        smtp.ehlo(mailInfo["hostname"])
        smtp.login(mailInfo["username"], mailInfo["password"])

        msg = MIMEText(mailInfo["mailtext"], 'plain', mailInfo['mailencoding'])
        msg["Subject"] = Header(mailInfo["mailsubject"], mailInfo["mailencoding"])
        msg["from"] = mailInfo["from"]
        msg["to"] = mailInfo["to"]
        smtp.sendmail(mailInfo["from"], mailInfo["to"], msg.as_string())
        smtp.quit()
    except Exception, e:
        print str(e)
