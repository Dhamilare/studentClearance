# Generated by Django 3.1.3 on 2020-11-15 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClearanceApp', '0002_auto_20201115_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='is_cleared',
            field=models.BooleanField(default=False),
        ),
    ]
