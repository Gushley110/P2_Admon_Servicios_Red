import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
# Define params


mailsender = "abraxassinclair1984@gmail.com"
mailreceip = "gushley110@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'xzjzPWgq'


def send_alert_attached(subject, host, tipo):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(host + tipo + ".png", 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    mserver = smtplib.SMTP(mailserver)
    mserver.starttls()
    # Login Credentials for sending the mail
    mserver.login(mailsender, password)

    mserver.sendmail(mailsender, mailreceip, msg.as_string())
    mserver.quit()

def test():
    msg = MIMEMultipart()
    msg['Subject'] = 'Test'
    msg['From'] = mailsender
    msg['To'] = mailreceip

    mserver = smtplib.SMTP(mailserver)
    mserver.starttls()
    # Login Credentials for sending the mail
    mserver.login(mailsender, password)

    mserver.sendmail(mailsender, mailreceip, 'Test')
    mserver.quit()

if __name__ == "__main__":
    test()