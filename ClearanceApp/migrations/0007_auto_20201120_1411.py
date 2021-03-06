# Generated by Django 3.1.3 on 2020-11-20 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClearanceApp', '0006_staff_staff_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['-id'], 'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
        migrations.AddField(
            model_name='clearance',
            name='department',
            field=models.CharField(choices=[('Pharmaceutical Technology', 'Pharmaceutical Technology'), ('Computer Science', 'Computer Science'), ('Statistics and Mathematics', 'Statistics and Mathematics'), ('Microbiology', 'Microbiology'), ('Food Technology', 'Food Technology'), ('Mass Communication', 'Mass Communication'), ('Urban & Regional Planning', 'Urban & Regional Planning'), ('Civil Engineering', 'Civil Engineering'), ('Business Administration', 'Business Administration'), ('Marketing', 'Marketing'), ('Accountancy', 'Accountancy')], default='Computer Science', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clearance',
            name='gender',
            field=models.CharField(choices=[('Female', 'Female'), ('Male', 'Male')], default='Female', max_length=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clearance',
            name='level',
            field=models.CharField(default='HND II', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clearance',
            name='matric_no',
            field=models.CharField(default='14/69/0109', max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
