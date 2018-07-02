from django.db import models
from django.core.exceptions import FieldError
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from dateutil.relativedelta import relativedelta

from kumon_student_db.student_registration import utils
from kumon_student_db.core import models as core_models


class MonthlyCost(models.Model):
    cost = models.IntegerField()
    effective_date = models.DateField(default=date.today)

    def __str__(self):
        return "<Cost: %d>, <Date: %s>" % (self.cost, self.effective_date)


class WhyChoice(models.Model):
    """Why the student is registering"""

    description = models.CharField(max_length=300)

    def __str__(self):
        return self.description


class HowChoice(models.Model):
    """How the student found out about Kumon"""

    description = models.CharField(max_length=300)

    def __str__(self):
        return self.description


class Parent(core_models.TimeStampedModel):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_address = models.EmailField()
    phone_number = PhoneNumberField(blank=False)


class Student(core_models.TimeStampedModel):
    BASE_REGISTRATION_COST = 50  # Dollars

    # TODO: turn these choices to Enums
    PRIMARY_DAY_CHOICES = (
        ("tues", "Tuesday"),
        ("sat", "Saturday"),
        ("tues_sat", "Tuesday & Saturday"),
    )

    LEVEL_CHOICES = (
        ("na", "N/A"),
        ("6a1", "6A1"),
        ("5a1", "5A1"),
        ("4a1", "4A1"),
        ("3a1", "3A1"),
        ("3a71", "3A71"),
        ("2a1", "2A1"),
        ("a1", "A1"),
        ("b1", "B1"),
        ("c1", "C1"),
        ("d1", "D1"),
        ("e1", "E1"),
    )

    # Contact Info
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    # Kumon Info
    start_date = models.DateField()
    primary_day = models.CharField(
        choices=PRIMARY_DAY_CHOICES,
        max_length=utils.len_longest_ith_item(PRIMARY_DAY_CHOICES, 0),
    )
    math_level = models.CharField(
        choices=LEVEL_CHOICES, max_length=utils.len_longest_ith_item(LEVEL_CHOICES, 0)
    )
    reading_level = models.CharField(
        choices=LEVEL_CHOICES, max_length=utils.len_longest_ith_item(LEVEL_CHOICES, 0)
    )

    why_choices = models.ManyToManyField(WhyChoice, blank=True)  # TODO: blank false
    how_choices = models.ManyToManyField(HowChoice, blank=True)  # TODO: blank false

    # Payment Info
    registration_discount_percent = core_models.SmallIntegerRangeField(
        min_value=0, max_value=100
    )
    registration_discount_reason = models.CharField(max_length=500, blank=True)

    payment_date = models.DateField(auto_now_add=True)  # TODO: lookup auto_now_add

    cash_paid = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    debit_paid = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    check_paid = models.DecimalField(max_digits=5, decimal_places=2, blank=True)
    credit_paid = models.DecimalField(max_digits=5, decimal_places=2, blank=True)

    check_number = models.CharField(max_length=50, blank=True)

    # Computed fields
    @property
    def n_subjects(self):
        return sum(
            1 if lvl != "na" else 0 for lvl in [self.math_level, self.reading_level]
        )

    @property
    def registration_cost(self):
        return (
            float(self.registration_discount_percent * self.BASE_REGISTRATION_COST)
            / 100
        )

    @property
    def sixth_month(self):
        d = self.start_date + relativedelta(months=6)  # TODO: should this be +6?
        return d.date()  # TODO: should this be d.date?

    @property
    def twelfth_month(self):
        d = self.start_date + relativedelta(months=12)  # TODO: should this be +6?
        return d.date()  # TODO: should this be d.date?

    @property
    def prorated_cost(self):
        # TODO
        return 0

    @property
    def monthly_cost(self):
        # TODO
        return 0

    @property
    def total_signup_cost(self):
        per_subj_cost = self.prorated_cost + (2 * self.monthly_cost)
        return self.registration_cost + (self.n_subjects * per_subj_cost)

    @property
    def total_paid(self):
        return self.cash_paid + self.debit_paid + self.check_paid + self.credit_paid

    def save(self, *args, **kwargs):
        if self.registration_discount_percent < 0 or self.registration_discount_percent > 100:
            raise FieldError('Registration discount must be in range [0,100].')
        super().save(*args, **kwargs)
