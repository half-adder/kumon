# Generated by Django 2.0.6 on 2018-07-18 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_registration', '0011_auto_20180718_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='reading_ppd',
            field=models.IntegerField(choices=[(5, 5), (10, 10), (20, 20)], default=10),
        ),
    ]
