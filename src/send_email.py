import smtplib
import os
from _datetime import datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders


def send_email(fullname, filename, email_adress):
    os.environ['GMAIL'] = "eqmhqfeyeiyimgub"
    fromaddr = 'noteespebot@gmail.com'

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = email_adress
    msg['Subject'] = "NoteEspeSett" + str(datetime.now().isocalendar()[1]) + " - di " + fullname + "."
    body = 'Ciao Steve, ecco note di questa settimana di ' + fullname + "\n Buon week end \n NoteEspeBot"
    msg.attach(MIMEText(body))
    files = [filename]

    for filename in files:
        attachment = open(filename, 'rb')
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition",
                        f"attachment; filename= {filename}")
        msg.attach(part)

    msg = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(fromaddr, os.environ['GMAIL'])
    server.sendmail(fromaddr, email_adress, msg)
    server.sendmail(fromaddr, "stevepostaFooBAr@gmail.com", msg)
    server.quit()
