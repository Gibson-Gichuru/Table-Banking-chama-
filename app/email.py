from threading import Thread
from flask import current_app, render_template
from . import  mail

from flask_mail import Message


def send_async_email(app, msg):

    pass

def send_email(to, subject, template, **kwargs):

    app = current_app._get_current_object()

    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + "" + subject, sender = app.config['MAIL_SENDER'], recepient = [to])

    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    thr = Thread(target=send_async_email, args=[app, msg])

    return thr