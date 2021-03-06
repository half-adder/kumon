# Generated by Django 2.0.6 on 2018-08-02 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_registration', '0022_delete_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='LobbyStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('school_year_start', models.IntegerField()),
                ('school_year_end', models.IntegerField()),
                ('grade', models.CharField(choices=[('pk-3', 'PK-3'), ('pk-2', 'PK-2'), ('pk-1', 'PK-1'), ('k', 'K'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('other', 'other')], max_length=10)),
                ('home_address', models.CharField(max_length=100)),
                ('apt_or_suite', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=10)),
                ('student_email', models.EmailField(max_length=254)),
                ('school', models.CharField(max_length=100)),
                ('parent_relation', models.CharField(choices=[('mother', 'Mother'), ('father', 'Father'), ('other', 'Other')], max_length=10)),
                ('parent_name', models.CharField(max_length=100)),
                ('parent_address', models.CharField(max_length=100)),
                ('parent_apt_or_suite', models.CharField(max_length=100)),
                ('parent_home_phone_number', models.CharField(max_length=10)),
                ('parent_mobile_phone_number', models.CharField(max_length=10)),
                ('parent_email', models.EmailField(max_length=254)),
                ('parent_state_province', models.CharField(max_length=100)),
                ('parent_zip_code', models.CharField(max_length=10)),
                ('emergency_name', models.CharField(max_length=100)),
                ('emergency_phone_number', models.CharField(max_length=10)),
                ('how_choices', models.ManyToManyField(blank=True, to='student_registration.HowChoice')),
                ('why_choices', models.ManyToManyField(blank=True, to='student_registration.WhyChoice')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
