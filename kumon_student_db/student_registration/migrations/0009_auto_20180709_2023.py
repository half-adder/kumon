# Generated by Django 2.0.6 on 2018-07-09 20:23

from django.db import migrations
import kumon_student_db.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('student_registration', '0008_auto_20180709_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='registration_discount_percent',
            field=kumon_student_db.core.models.SmallIntegerRangeField(default=0),
        ),
    ]