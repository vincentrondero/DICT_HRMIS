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
    time_in = models.TimeField(null=True)
    time_out = models.TimeField(null=True)
    minutes_late = models.IntegerField(null=True, blank=True)
    undertime_hours = models.IntegerField(null=True, blank=True)
    undertime_minutes = models.IntegerField(null=True, blank=True)
    excel_file = models.ForeignKey(CleansedData, on_delete=models.CASCADE, null=True, blank=True)
    
    REMARK_CHOICES = [
        ('FULL', 'Full Day'),
        ('HALF', 'Half Day'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late'),
        ('HOLIDAY', 'Holiday'),
        ('LEAVE', 'Leave'),
    ]

    remark = models.CharField(max_length=7, choices=REMARK_CHOICES)
    generated_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.employee.username} - {self.date} - {self.get_remark_display()}"

    
class Payslip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    basic_salary = models.FloatField(default=0.0)
    premium = models.FloatField(default=0.0)
    gross_pay = models.FloatField(default=0.0)
    daily_salary = models.FloatField(default=0.0)
    total_late_minutes = models.IntegerField(default=0)
    late_attendance_count = models.IntegerField(default=0)
    late_deduction = models.FloatField(default=0.0)
    absent_count = models.IntegerField(default=0)
    absent_deduction = models.FloatField(default=0.0)
    pre_deduction = models.FloatField(default=0.0)
    total_deduction = models.FloatField(default=0.0)
    net_before_tax = models.FloatField(default=0.0)
    tax_2_percent = models.FloatField(default=0.0)
    tax_3_percent = models.FloatField(default=0.0)
    number_of_days = models.IntegerField(default=0)
    date_range = models.CharField(max_length=255)
    total_net_pay = models.FloatField(default=0.0)
    current_date = models.DateField(default=timezone.now)
    activated_date = models.DateTimeField(default=timezone.now)
    activated = models.BooleanField(default=True)
    cooperative_deduction = models.FloatField(default=0.0)
    member_status = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user.username} - {self.activated}"

    
class SalaryGrade(models.Model):
    grade = models.CharField(max_length=2, unique=True)
    salary = models.FloatField()

    def __str__(self):
        return f"Grade {self.grade} -  ₱{self.salary}"