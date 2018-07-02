from datetime import datetime

import factory
from faker import Faker
import random

from kumon_student_db.student_registration import models

fake = Faker()


class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Parent

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email_address = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    created = datetime.now()
    modified = datetime.now()


class WhyChoiceFactory(factory.django.DjangoModelFactory):
    description = "Just thought it'd be good"


class HowChoiceFactory(factory.django.DjangoModelFactory):
    description = "Google"


class MonthlyCostFactory(factory.django.DjangoModelFactory):
    cost = 100
    effective_date = factory.Faker("date_time_this_century")


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Student

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    parent = factory.SubFactory(ParentFactory)

    start_date = fake.date_time_between(start_date="-5y", end_date="+5y", tzinfo=None)
    primary_day = "tues"
    math_level = models.Student.LEVEL_CHOICES[
        random.randint(0, len(models.Student.LEVEL_CHOICES) - 1)
    ][0]
    reading_level = models.Student.LEVEL_CHOICES[
        random.randint(0, len(models.Student.LEVEL_CHOICES) - 1)
    ][0]

    # why_choices = None  # TODO
    # how_choices = None  # TODO

    registration_discount_percent = random.randint(1, 100)
    registration_discount_reason = "Some random reason"

    payment_date = datetime.today()

    cash_paid = 0.0
    debit_paid = 0.0
    check_paid = 0.0
    credit_paid = 0.0

    check_number = "0790"

    created = datetime.now()
    modified = datetime.now()
