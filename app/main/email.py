from flask import render_template
from app.email import send_email


def send_contact_email(form):
    send_email(f'[TraceyNicholasArt] Message from {form.name.data}',
        sender=(form.name.data, form.email.data),
        recipients=['info@traceynicholas.com'],
        text_body=render_template('email/contact_me.txt', msg=form.msg.data),
        html_body=render_template('email/contact_me.html', msg=form.msg.data))
        