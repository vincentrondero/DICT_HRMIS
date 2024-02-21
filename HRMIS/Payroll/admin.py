from django.contrib import admin
from .models import CleansedData, Attendance, Payslip

admin.site.register(CleansedData)
admin.site.register(Attendance)
admin.site.register(Payslip)

