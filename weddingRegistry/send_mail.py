from flask_mail import Message
from weddingRegistry import mail
from weddingRegistry import app
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template_body):
    msg = Message(subject,
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[to])
    # msg.body = txt_body
    msg.html = template_body
    Thread(target=send_async_email, args=(app, msg)).start()
