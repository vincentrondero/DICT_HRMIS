from django.contrib.auth.hashers import make_password
from django.db import models

class User(models.Model):
    USER_pkID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    
    ROLE_CHOICES = [
        ('HR', 'HR'),
        ('JO', 'JO'),
    ]
    
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    salary_grade = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
