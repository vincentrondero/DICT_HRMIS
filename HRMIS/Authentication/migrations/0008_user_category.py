# Generated by Django 5.0.2 on 2024-04-25 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0007_user_cooperative_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='category',
            field=models.CharField(choices=[('TOD', 'TOD'), ('FOD', 'FOD')], default='TOD', max_length=3),
        ),
    ]
