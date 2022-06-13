from django.db import models
from users.models import CustomUser

# Create your models here.
class EmailVerification(models.Model):
    user = models.OneToOneField(CustomUser, blank=False, unique=True, on_delete=models.CASCADE)
    verification_code = models.IntegerField()
    verified = models.BooleanField(default=False,blank=False)

    def __str__(self):
        return self.user.email