import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

email = 'dossymkhanova.a@gmail.com'

def send_email(email, subject, text, attachment_path, attachment_path2 ):
    port = 465
    smtp_server = "smtp.yandex.ru"
    sender_email = "noreply.akd@yandex.ru"
    sender_password = "sktdggqupaveyhot"
    receiver_email = email

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Attach the text message
    msg.attach(MIMEText(text, 'plain'))

 # Attach the first DOCX document
    with open(attachment_path, 'rb') as file:
        docx_attachment = MIMEApplication(file.read(), _subtype="docx")
        docx_attachment.add_header(
            'content-disposition', 'attachment', filename=os.path.basename(attachment_path)
        )
        msg.attach(docx_attachment)

    # Attach the second DOCX document
    with open(attachment_path2, 'rb') as file:
        docx_attachment2 = MIMEApplication(file.read(), _subtype="docx")
        docx_attachment2.add_header(
            'content-disposition', 'attachment', filename=os.path.basename(attachment_path2)
        )
        msg.attach(docx_attachment2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        # print('OKK')
        return("Успешно отправлено!")

# Specify the path to your DOCX file here
# docx_attachment_path = './new_resume.docx'
# docx_attachment_path2 = './sample_resume2.docx'

# send_email(email, 'New resume', 'Hello, please find the resume attached.', docx_attachment_path,docx_attachment_path2)
