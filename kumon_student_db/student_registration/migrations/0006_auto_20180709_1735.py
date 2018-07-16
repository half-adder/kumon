# Generated by Django 2.0.6 on 2018-07-09 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("student_registration", "0005_auto_20180706_2119")]

    operations = [
        migrations.RemoveField(model_name="student", name="first_name"),
        migrations.RemoveField(model_name="student", name="last_name"),
        migrations.RemoveField(model_name="student", name="parent"),
        migrations.AddField(
            model_name="student",
            name="email",
            field=models.EmailField(default="seanjohnsen96@gmail.com", max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="student",
            name="name",
            field=models.CharField(default="Sean Johnsen", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="student",
            name="parent_name",
            field=models.CharField(default="Brian Johnsen", max_length=100),
            preserve_default=False,
        ),
    ]
