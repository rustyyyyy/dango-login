import os
from pathlib import Path
import environ
import requests

from config.models import EmailVerification

from .models import CustomUser

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)

api_key = env("api_key")

def captcha_validation(recaptcha_response=None, secret=None):
    data = {"secret": secret, "response": recaptcha_response}

    r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
    result = r.json()

    if result["success"]:
        return True

    return False


def email_verification(email=None):
    import json
    import random

    otp_code = random.randint(11111, 99999)

    user = CustomUser.objects.get(email=email)
    new_user = EmailVerification(user=user, verification_code=otp_code, verified=False)
    new_user.save()

    url = "https://api.sendinblue.com/v3/smtp/email"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-key": api_key,
    }

    data = {
        "body": "hello",
        "sender": {"name": "admin@cs_login", "email": "ajul@ismt.edu.np"},
        "subject": "Email Verification",
        "to": [{"email": f"{email}", "name": "test_name"}],
        "textContent": f"Your verification code is {otp_code}",
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    print(response)

    if response.status_code == 201:
        user = CustomUser.objects.get(email=email)
        user_id = EmailVerification.objects.get(user=user).id

        return user_id
    return False
