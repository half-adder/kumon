from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView

from kumon_student_db.student_registration import models, forms


class StudentList(ListView):
    model = models.Student


class StudentDetail(DetailView):
    model = models.Student

    def get_object(self, queryset=models.Student.objects.all()):
        return super().get_object()


class StudentForm(FormView):
    template_name = 'student_registration/student_form.html'
    form_class = forms.StudentForm
    success_url = '/'


class ParentList(ListView):
    model = models.Parent


class ParentDetail(DetailView):
    model = models.Parent

    def get_object(self, queryset=models.Parent.objects.all()):
        return super().get_object()
