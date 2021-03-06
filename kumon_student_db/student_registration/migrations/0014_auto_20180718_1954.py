# Generated by Django 2.0.6 on 2018-07-18 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_registration', '0013_student_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='math_level',
            field=models.CharField(blank=True, choices=[('7a1', '7A1'), ('6a1', '6A1'), ('5a1', '5A1'), ('4a1', '4A1'), ('3a1', '3A1'), ('3a71', '3A71'), ('2a1', '2A1'), ('a1', 'A1'), ('b1', 'B1'), ('c1', 'C1'), ('d1', 'D1'), ('e1', 'E1')], max_length=4),
        ),
        migrations.AlterField(
            model_name='student',
            name='reading_level',
            field=models.CharField(blank=True, choices=[('7a1', '7A1'), ('6a1', '6A1'), ('5a1', '5A1'), ('4a1', '4A1'), ('3a1', '3A1'), ('3a71', '3A71'), ('2a1', '2A1'), ('a1', 'A1'), ('b1', 'B1'), ('c1', 'C1'), ('d1', 'D1'), ('e1', 'E1')], max_length=4),
        ),
    ]
