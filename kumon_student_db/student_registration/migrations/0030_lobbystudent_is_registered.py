# Generated by Django 2.0.6 on 2018-08-03 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_registration', '0029_auto_20180803_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobbystudent',
            name='is_registered',
            field=models.BooleanField(default=False),
        ),
    ]
