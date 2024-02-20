from django.db import models
from Authentication.models import User
from django.utils import timezone

class CleansedData(models.Model):
    file_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_binary = models.BinaryField()

    def __str__(self):
        return self.file_name

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    excel_file = models.ForeignKey(CleansedData, on_delete=models.CASCADE, null=True, blank=True)
    
    REMARK_CHOICES = [
        ('FULL', 'Full Day'),
        ('HALF', 'Half Day'),
        ('ABSENT', 'Absent'),
    ]

    remark = models.CharField(max_length=6, choices=REMARK_CHOICES)
    generated_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.employee.username} - {self.date} - {self.get_remark_display()}"