# Generated by Django 3.1.3 on 2020-11-25 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ClearanceApp', '0024_auto_20201125_2227'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='user',
            new_name='staff',
        ),
    ]
