# Generated by Django 5.0.2 on 2024-02-20 07:07

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0006_alter_profile_profile_picture'),
        ('Payroll', '0004_attendance_generated_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payslip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monthly_salary', models.FloatField()),
                ('full_attendance_count', models.IntegerField()),
                ('half_attendance_count', models.IntegerField()),
                ('absent_attendance_count', models.IntegerField()),
                ('date_range', models.CharField(max_length=255)),
                ('activated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('activated', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Authentication.user')),
            ],
        ),
    ]
