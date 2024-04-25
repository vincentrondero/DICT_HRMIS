from django.contrib.auth.hashers import make_password, check_password
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
    archived = models.BooleanField(default=False)
    cooperative_member = models.BooleanField(default=False)
    category = models.CharField(max_length=3, choices=[('TOD', 'TOD'), ('FOD', 'FOD')], default='TOD') 

    def save(self, *args, **kwargs):
        if self.archived:
            super().save(*args, **kwargs)
        elif not self._state.adding and not check_password(self.password, make_password('dummy')):
            if self.password != User.objects.get(pk=self.pk).password:
                self.password = make_password(self.password)
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.BinaryField(null=True, blank=True)
