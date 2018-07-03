from django.shortcuts import render
from django.views.generic import ListView
from kumon_student_db.student_registration import models


class StudentList(ListView):
    model = models.Student
