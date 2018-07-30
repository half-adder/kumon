import django_tables2 as tables
from kumon_student_db.student_registration import models


class StudentTable(tables.Table):
    class Meta:
        model = models.Student
        fields = (
            "name",
            "parent_name",
            "email",
            "phone",
            "start_date",
            "total_signup_cost",
            "total_paid",
        )
        orderable = False

