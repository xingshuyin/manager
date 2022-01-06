from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=128)
    comment = models.CharField(max_length=100)


class User(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)


class Token(models.Model):
    user = models.OneToOneField(to="User", on_delete=models.CASCADE)
    token = models.CharField(max_length=200)
