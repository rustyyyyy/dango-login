from django.contrib import admin

from config.models import EmailVerification


@admin.register(EmailVerification)
class EmailVerification(admin.ModelAdmin):
    model = EmailVerification
    list_display = ["user", "verification_code", "verified"]
