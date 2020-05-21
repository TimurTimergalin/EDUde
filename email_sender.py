import smtplib

from email.message import EmailMessage


def sendmessage(student_name, student_class, task_name, teacher_email, text, files=None):
    print(files)
    msg = EmailMessage()
    msg.set_content(text)
    if files:
        for file in files:
            msg.add_attachment(file[2], maintype=file[0], subtype=file[1])
    msg['Subject'] = f'{student_name}, {student_class}, {task_name}'
    msg['From'] = 'edudebot@yandex.ru'
    msg['To'] = teacher_email
    server = smtplib.SMTP_SSL('smtp.yandex.ru')
    server.login('edudebot@yandex.ru', 'qwertyPASSWORD123')
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    sendmessage('Gleb', 'Math', 'DZ 23.04', 'gleb-petuhov@mail.ru', 'asd', [open('1.jpg', 'rb').read()])
