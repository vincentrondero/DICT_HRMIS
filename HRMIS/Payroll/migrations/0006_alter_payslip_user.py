# Generated by Django 5.0.2 on 2024-02-20 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0006_alter_profile_profile_picture'),
        ('Payroll', '0005_payslip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payslip',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Authentication.user', to_field='username'),
        ),
    ]
