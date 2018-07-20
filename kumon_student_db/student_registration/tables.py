import django_tables2 as tables
from django.conf.urls import url
from django.urls import reverse_lazy
from django.utils.html import format_html
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
        attrs = {"id": "id_student_table",}
        orderable = False

    def render_name(self, value):
        return format_html('<a href={link}>{name}</a>', link=reverse_lazy('student-update', ), name=value)
