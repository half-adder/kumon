# Generated by Django 2.0.6 on 2018-07-09 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_registration', '0009_auto_20180709_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='cash_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='student',
            name='check_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='student',
            name='credit_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='student',
            name='debit_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]