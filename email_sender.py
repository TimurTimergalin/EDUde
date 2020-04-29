import smtplib

from email.message import EmailMessage
from PIL import Image


def sendmessage(student_name, student_class, task_name, teacher_email, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = f'{student_name}, {student_class}, {task_name}'
    msg['From'] = 'email@mail.ru'
    msg['To'] = teacher_email
    server = smtplib.SMTP_SSL('smtp.mail.ru')
    server.login('email@mail.ru', 'password')
    server.send_message(msg)
    server.quit()


# content = Image.open('1.jpg')
sendmessage('Gleb', 'Math', 'DZ 23.04', 'email@gmail.com', content)