from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView

from kumon_student_db.student_registration import models, forms, utils


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


# API Functions
def prorated_cost(request, start_date):
    """Return the prorated cost for the given date

    TODO: test this
    """
    monthly_cost = models.MonthlyCost.get_cost_for(start_date)
    return utils.prorated_cost(start_date, monthly_cost)
