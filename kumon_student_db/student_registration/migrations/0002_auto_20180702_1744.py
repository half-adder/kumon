# Generated by Django 2.0.6 on 2018-07-02 17:44

from django.db import migrations, models
import django.utils.timezone
import kumon_student_db.core.models


class Migration(migrations.Migration):

    dependencies = [("student_registration", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="student", name="date_form_generated"),
        migrations.AddField(
            model_name="parent",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="parent",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="student",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="student",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="student",
            name="how_choices",
            field=models.ManyToManyField(
                blank=True, to="student_registration.HowChoice"
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="registration_discount_percent",
            field=kumon_student_db.core.models.SmallIntegerRangeField(),
        ),
        migrations.AlterField(
            model_name="student",
            name="why_choices",
            field=models.ManyToManyField(
                blank=True, to="student_registration.WhyChoice"
            ),
        ),
    ]
