# Generated by Django 3.1.3 on 2020-11-22 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ClearanceApp', '0010_remove_clearance_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='clearance',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ClearanceApp.student'),
            preserve_default=False,
        ),
    ]