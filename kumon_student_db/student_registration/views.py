from django.shortcuts import render
from django.views.generic import ListView, DetailView
from kumon_student_db.student_registration import models


class StudentList(ListView):
    model = models.Student


class StudentDetail(DetailView):
    model = models.Student

    def get_object(self, queryset=models.Student.objects.all()):
        return super().get_object()
