# Generated by Django 3.1.3 on 2020-11-20 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClearanceApp', '0008_clearance_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='clearance',
            name='other_names',
            field=models.CharField(default='Oluwaseun', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clearance',
            name='surname',
            field=models.CharField(default='Babatunde', max_length=100),
            preserve_default=False,
        ),
    ]