import os
from pathlib import Path
from urllib import parse

import environ
from config.models import EmailVerification
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from users.forms import CustomUserCreationForm
from users.helper import captcha_validation, email_verification

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)

secret = env("secret")
site_key = env("site_key")

import time


class SignupView(View):
    def get(self, request):
        return render(
            request,
            "index.html",
            {"form": CustomUserCreationForm, "site_key": site_key},
        )

    def post(self, request):
        form = CustomUserCreationForm(request.POST)

        recaptcha_response = request.POST.get("g-recaptcha-response")

        if captcha_validation(recaptcha_response, secret):
            if form.is_valid():
                email = form.data["email"]
                form.save()

                verification = email_verification(email)

                if verification:
                    return redirect(f"/emailverify/{verification}")
                return render(
                    request,
                    "index.html",
                    {"message": "Error in email verification.", "site_key": site_key},
                )

            return render(request, "index.html", {"form": form, "site_key": site_key})
        return render(
            request,
            "index.html",
            {"message": "Invalid reCAPTCHA. Please try again.", "site_key": site_key},
        )


class EmailVerify(View):
    def get(self, request, pk=None):
        referer = request.META.get("HTTP_REFERER")
        path = parse.urlparse(referer).path

        if path == "/signup/":
            return render(request, "emailverify.html")
        return redirect("/")

    def post(self, request, pk=None):
        try:
            code = request.POST.get("code")
            user = get_object_or_404(EmailVerification, pk=pk)

            if user.verification_code == int(code):
                user.verified = True
                user.save()

                time.sleep(1)
                return redirect("/")

            return render(request, "emailverify.html", {"message": "Incorrect Otp"})

        except:
            return render(
                request,
                "emailverify.html",
                {"message": "Error occured while verification."},
            )