# Generated by Django 2.0.6 on 2018-08-02 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_registration', '0023_lobbystudent'),
    ]

    operations = [
        migrations.AddField(
            model_name='lobbystudent',
            name='student_city',
            field=models.CharField(default='Birmingham', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lobbystudent',
            name='student_state_province',
            field=models.CharField(default='AL', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lobbystudent',
            name='student_zip_code',
            field=models.CharField(default=35244, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lobbystudent',
            name='parent_home_phone_number',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='lobbystudent',
            name='phone_number',
            field=models.CharField(max_length=14),
        ),
    ]