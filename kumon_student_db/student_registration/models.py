from django.db import models
from django.core.exceptions import FieldError
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from dateutil.relativedelta import relativedelta

from kumon_student_db.student_registration import utils
from kumon_student_db.core import models as core_models


class MonthlyCost(models.Model):
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    effective_date = models.DateField(default=date.today)

    @staticmethod
    def get_cost_for(start_date):
        return (
            MonthlyCost.objects.filter(effective_date__lt=start_date)
            .order_by("-effective_date")
            .first()
            .cost
        )

    def __str__(self):
        return "Monthly Cost: %.2f, Effective Date: %s" % (float(self.cost), self.effective_date)
        # return f"<Cost: {self.cost:d}>, <Date: {self.effective_date}>"


class RegistrationCost(models.Model):
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    effective_date = models.DateField(default=date.today)

    @staticmethod
    def get_cost_for(start_date):
        return (
            RegistrationCost.objects.filter(effective_date__lt=start_date)
            .order_by("-effective_date")
            .first()
            .cost
        )

    def __str__(self):
        return "Registration Cost: %.2f, Effective Date: %s" % (float(self.cost), self.effective_date)


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

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Student(core_models.TimeStampedModel):

    # TODO: turn these choices to Enums
    PRIMARY_DAY_CHOICES = (
        ("tues", "Tuesday"),
        ("sat", "Saturday"),
        ("tues_sat", "Tuesday & Saturday"),
    )

    LEVEL_CHOICES = (
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
    name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    email = models.EmailField()

    # Kumon Info
    start_date = models.DateField()
    primary_day = models.CharField(
        choices=PRIMARY_DAY_CHOICES,
        max_length=utils.len_longest_ith_item(PRIMARY_DAY_CHOICES, 0),
    )
    math_level = models.CharField(
        choices=LEVEL_CHOICES,
        max_length=utils.len_longest_ith_item(LEVEL_CHOICES, 0),
        blank=True,
    )
    reading_level = models.CharField(
        choices=LEVEL_CHOICES,
        max_length=utils.len_longest_ith_item(LEVEL_CHOICES, 0),
        blank=True,
    )

    why_choices = models.ManyToManyField(WhyChoice, blank=True)  # TODO: blank false
    how_choices = models.ManyToManyField(HowChoice, blank=True)  # TODO: blank false

    # Payment Info
    registration_discount_percent = core_models.SmallIntegerRangeField(
        # TODO just make this a small integer field?
        default=0,
        min_value=0,
        max_value=100,
    )
    registration_discount_reason = models.CharField(max_length=500, blank=True)

    payment_date = models.DateField(auto_now_add=True)  # TODO: lookup auto_now_add

    cash_paid = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    debit_paid = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    check_paid = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    credit_paid = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    check_number = models.CharField(max_length=50, blank=True)

    # Computed fields
    @property
    def n_subjects(self):
        return sum(
            1 if lvl else 0 for lvl in [self.math_level, self.reading_level]
        )

    @property
    def registration_cost(self):
        base_registration_cost = RegistrationCost.get_cost_for(self.start_date)
        return (
            float((100 - self.registration_discount_percent) * base_registration_cost)
            / 100
        )

    @property
    def sixth_month(self):
        return self.start_date + relativedelta(months=+6)

    @property
    def twelfth_month(self):
        return self.start_date + relativedelta(months=+12)

    @property
    def prorated_first_month_cost(self):
        """
        Returns the prorated cost for the first month.

        The prorated cost is defined relative to the starting date as such:

            floor((PDL / TPD) * C)

        where
            PDL = Primary Days Left in Month
            TPD = Total Primary Days in Month
            C = Monthly Cost

        TODO: I bet that enum refactor will make this nicer
        """
        return utils.prorated_cost(self.start_date, self.monthly_cost)

    @property
    def monthly_cost(self):
        return MonthlyCost.get_cost_for(self.start_date)

    @property
    def per_subject_cost(self):
        return self.prorated_first_month_cost + (2 * self.monthly_cost)

    @property
    def total_signup_cost(self):
        return float(self.registration_cost) + float(self.n_subjects * self.per_subject_cost)

    @property
    def total_paid(self):
        return self.cash_paid + self.credit_paid + self.debit_paid + self.check_paid

    @property
    def is_fully_paid(self):
        return self.total_paid >= self.total_signup_cost

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if (
            self.registration_discount_percent < 0
            or self.registration_discount_percent > 100
        ):
            raise FieldError("Registration discount must be in range [0,100].")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
