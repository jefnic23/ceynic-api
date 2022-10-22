import requests
from flask import current_app


def send_email(subject, sender, text_body, html_body):
    return requests.post(
        f'https://api.mailgun.net/v3/{current_app.config["MAIL_DOMAIN"]}/messages',
        auth=("api", current_app.config["MAIL_API_KEY"]),
        data={
            "subject": subject,
            "from": f"{sender[0]} {sender[1]}",
            "to": [current_app.config['EMAIL_RECIPIENT']],
            "text": text_body,
            "html": html_body
        }
    )
