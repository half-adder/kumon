import pytest
from kumon_student_db.student_registration.tests import factories
from kumon_student_db.student_registration.models import Student

pytestmark = pytest.mark.django_db


def test_student_factory_creation():
    student = factories.StudentFactory()


def test_student_0_subjects_if_na_for_both():
    student = factories.StudentFactory(math_level=Student.LEVEL_CHOICES[0][0], reading_level=Student.LEVEL_CHOICES[0][0])
    assert student.n_subjects == 0


def test_student_1_subj_if_only_reg_math():
    student = factories.StudentFactory(math_level=Student.LEVEL_CHOICES[1][0], reading_level=Student.LEVEL_CHOICES[0][0])
    assert student.n_subjects == 1


def test_student_1_subj_if_only_reg_reading():
    student = factories.StudentFactory(math_level=Student.LEVEL_CHOICES[0][0], reading_level=Student.LEVEL_CHOICES[1][0])
    assert student.n_subjects == 1


def test_student_2_subj_if_reg_reading_and_math():
    student = factories.StudentFactory(math_level=Student.LEVEL_CHOICES[1][0], reading_level=Student.LEVEL_CHOICES[1][0])
    assert student.n_subjects == 2
