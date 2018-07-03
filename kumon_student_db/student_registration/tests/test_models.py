import datetime
from dateutil.relativedelta import relativedelta
from django.core.exceptions import FieldError
import pytest
from kumon_student_db.student_registration.tests import factories
from kumon_student_db.student_registration.models import Student, MonthlyCost

pytestmark = pytest.mark.django_db


def test_student_factory_creation():
    student = factories.StudentFactory()


def test_student_0_subjects_if_na_for_both():
    student = factories.StudentFactory(
        math_level=Student.LEVEL_CHOICES[0][0],
        reading_level=Student.LEVEL_CHOICES[0][0],
    )
    assert student.n_subjects == 0


def test_student_1_subj_if_only_reg_math():
    student = factories.StudentFactory(
        math_level=Student.LEVEL_CHOICES[1][0],
        reading_level=Student.LEVEL_CHOICES[0][0],
    )
    assert student.n_subjects == 1


def test_student_1_subj_if_only_reg_reading():
    student = factories.StudentFactory(
        math_level=Student.LEVEL_CHOICES[0][0],
        reading_level=Student.LEVEL_CHOICES[1][0],
    )
    assert student.n_subjects == 1


def test_student_2_subj_if_reg_reading_and_math():
    student = factories.StudentFactory(
        math_level=Student.LEVEL_CHOICES[1][0],
        reading_level=Student.LEVEL_CHOICES[1][0],
    )
    assert student.n_subjects == 2


def test_registration_discount_non_negative():
    with pytest.raises(FieldError):
        student = factories.StudentFactory(registration_discount_percent=-1)
        student.save()


def test_registration_discount_max_100():
    with pytest.raises(FieldError):
        student = factories.StudentFactory(registration_discount_percent=101)
        student.save()


def test_6th_month():
    student = factories.StudentFactory()
    delta = relativedelta(student.start_date, student.sixth_month)
    assert abs(delta.months) == 6


def test_6th_month_returns_date():
    student = factories.StudentFactory()
    assert type(student.sixth_month) is datetime.date


def test_12th_month():
    student = factories.StudentFactory()
    delta = relativedelta(student.start_date, student.twelfth_month)
    assert abs(delta.years * 12 + delta.months) == 12


def test_12th_month_returns_date():
    student = factories.StudentFactory()
    assert type(student.twelfth_month) is datetime.date


def test_prorated_cost_unaffected_by_primary_day():
    MonthlyCost.objects.create(cost=105, effective_date=datetime.date(1000, 1, 1))

    student_tues = factories.StudentFactory(primary_day="tues")
    student_sat = factories.StudentFactory(primary_day="sat")
    student_tues_sat = factories.StudentFactory(primary_day="tues_sat")

    students = [student_tues, student_sat, student_tues_sat]

    assert all(
        student.prorated_first_month_cost == students[0].prorated_first_month_cost
        for student in students
    )
