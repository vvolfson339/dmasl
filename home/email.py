import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def sent_commission_email(org, member):
    fromaddr = "dmasl_enrolment@volfson.ca"
    toaddr = "#"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr

    msg['Subject'] = ""


    body = """
    
    """.format()

    msg.attach(MIMEText(body, 'html'))


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(fromaddr, "menaKP00")

    text = msg.as_string()

    server.sendmail(fromaddr, toaddr, text)
    server.quit()
