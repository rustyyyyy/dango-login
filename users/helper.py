import os
from pathlib import Path

import environ
import requests
import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail

from config.models import EmailVerification

from .models import CustomUser

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)


def captcha_validation(recaptcha_response=None, secret=None):
    data = {"secret": secret, "response": recaptcha_response}

    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
    result = r.json()

    if result["success"]:
        return True

    return False


def email_verification(email=None):
    import random

    otp_code = random.randint(11111, 99999)

    user = CustomUser.objects.get(email=email)
    new_user = EmailVerification(user=user, verification_code=otp_code, verified=False)
    new_user.save()

    sg = sendgrid.SendGridAPIClient(api_key=env("SENDGRID_API_KEY"))
    from_email = Email(env("sendgrid_from_email"))

    subject = "Email verification"
    content = Content("text/plain", "Your verification code is " + str(otp_code))
    mail = Mail(from_email, email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)

    # print(response.status_code)

    if response.status_code == 202:
        user = CustomUser.objects.get(email=email)
        user_id = EmailVerification.objects.get(user=user).id

        return user_id
    return False
