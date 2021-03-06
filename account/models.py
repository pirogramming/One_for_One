from django.db import models
from django.contrib.auth.models import User


class Univ(models.Model):
    name = models.TextField(max_length=255)
    addr = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.TextField(max_length=10)
    univ = models.ForeignKey(Univ, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, default='01000000000')
    good_review = models.IntegerField(default=0)
    bad_review = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class AuthSms(models.Model):
    phone_number = models.CharField(max_length=20, primary_key=True)
    auth_number = models.IntegerField()

    class Meta:
        db_table = 'auth_numbers'
