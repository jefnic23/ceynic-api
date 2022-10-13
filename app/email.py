from flask_mail import Message
from threading import Thread
from flask import current_app
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = f'{text_body}\n{sender[0]} {sender[1]}'
    msg.html = f'{html_body}\n{sender[0]} {sender[1]}' 
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
