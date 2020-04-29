import imghdr
import smtplib

from email.message import EmailMessage


def sendmessage(student_name, student_class, task_name, teacher_email, text, files=None):
    if files is None:
        files = []
    msg = EmailMessage()
    msg.set_content(text)
    for file in files:
        msg.add_attachment(file, maintype='image', subtype=imghdr.what(None, file))
    msg['Subject'] = f'{student_name}, {student_class}, {task_name}'
    msg['From'] = 'edudebot@yandex.ru'
    msg['To'] = teacher_email
    server = smtplib.SMTP_SSL('smtp.yandex.ru')
    server.login('edudebot@yandex.ru', 'qwertyPASSWORD123')
    server.send_message(msg)
    server.quit()


# sendmessage('Gleb', 'Math', 'DZ 23.04', 'gleb-petuhov@mail.ru', 'asd', [open('1.jpg', 'rb').read()])
