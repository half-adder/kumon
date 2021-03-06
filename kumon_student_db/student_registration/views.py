import datetime
import logging

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.http import HttpResponse

from kumon_student_db.student_registration import models, forms

logger = logging.getLogger(__name__)


class StudentApplicationCreate(CreateView):
    form_class = forms.StudentApplicationForm
    template_name = "student_registration/student_application_form.html"
    queryset = models.LobbyStudent.objects.all()
    success_url = reverse_lazy("student_registration:student-application-create")


class StudentApplicationUpdate(UpdateView):
    form_class = forms.StudentApplicationForm
    template_name = "student_registration/student_application_form.html"
    queryset = models.LobbyStudent.objects.all()
    success_url = reverse_lazy("student_registration:student-application-list")


class StudentApplicationDelete(DeleteView):
    model = models.LobbyStudent
    success_url = reverse_lazy("student_registration:student-application-list")
    template_name = "student_registration/student_confirm_delete.html"


class StudentApplicationList(ListView):
    model = models.LobbyStudent
    template_name = "student_registration/student_application_list.html"


class StudentList(ListView):
    model = models.Student


class StudentCreate(CreateView):
    form_class = forms.StudentForm
    template_name = "student_registration/student_form_crispy.html"
    queryset = models.Student.objects.all()

    def get_success_url(self):
        if "print" in self.request.POST:
            return reverse_lazy(
                "student_registration:customer-copy", kwargs={"pk": self.object.pk}
            )
        else:
            return reverse_lazy("student_registration:student-list")

    def get_initial(self):
        if self.request.GET.get('app_id', ''):
            app_obj = get_object_or_404(models.LobbyStudent, id=self.request.GET['app_id'])
            return {
                'name': app_obj.name,
                'parent_name': app_obj.parent_name,
                'email': app_obj.parent_email if app_obj.parent_email else app_obj.student_email,
                'phone': app_obj.parent_mobile_phone_number if app_obj.parent_mobile_phone_number else app_obj.parent_home_phone_number,
                'how_choices': app_obj.how_choices.all(),
                'why_choices': app_obj.why_choices.all(),
                'instructor': 1,
                'application': self.request.GET['app_id']
            }
        else:
            return {}


class StudentUpdate(UpdateView):
    form_class = forms.StudentForm
    template_name = "student_registration/student_form_crispy.html"
    queryset = models.Student.objects.all()

    def get_success_url(self):
        if "print" in self.request.POST:
            return reverse_lazy(
                "student_registration:customer-copy", kwargs={"pk": self.object.pk}
            )
        else:
            return reverse_lazy("student_registration:student-list")


class StudentDelete(DeleteView):
    model = models.Student
    success_url = reverse_lazy("student_registration:student-list")


def cost_list(request):
    if request.method != "GET":
        return HttpResponse(status=404)  # TODO: better error code

    monthly_costs = models.MonthlyCost.objects.all()
    reg_costs = models.RegistrationCost.objects.all()

    return render(
        request,
        template_name="student_registration/costs_list.html",
        context={"monthly_costs": monthly_costs, "reg_costs": reg_costs},
    )


def customer_copy(request, pk):
    student = get_object_or_404(models.Student, pk=pk)
    time = datetime.date.today()
    return render(
        request,
        template_name="student_registration/customer_copy2.html",
        context={"student": student, 'time': time},
    )


def choices(request):
    how_choices = models.HowChoice.objects.all()
    why_choices = models.WhyChoice.objects.all()
    return render(
        request,
        template_name="student_registration/choices.html",
        context={"how_choices": how_choices, "why_choices": why_choices},
    )


class HowChoiceCreateView(CreateView):
    form_class = forms.HowChoiceForm
    template_name = "student_registration/choice_form.html"
    success_url = reverse_lazy("student_registration:choices")
    queryset = models.HowChoice.objects.all()


class WhyChoiceCreateView(CreateView):
    form_class = forms.WhyChoiceForm
    template_name = "student_registration/choice_form.html"
    success_url = reverse_lazy("student_registration:choices")
    queryset = models.WhyChoice.objects.all()


class HowChoiceUpdateView(UpdateView):
    model = models.HowChoice
    form_class = forms.HowChoiceForm
    template_name = "student_registration/choice_form.html"
    success_url = reverse_lazy("student_registration:choices")
    queryset = models.HowChoice.objects.all()


class WhyChoiceUpdateView(UpdateView):
    model = models.WhyChoice
    form_class = forms.WhyChoiceForm
    template_name = "student_registration/choice_form.html"
    success_url = reverse_lazy("student_registration:choices")
    queryset = models.WhyChoice.objects.all()


class HowChoiceDeleteView(DeleteView):
    model = models.HowChoice
    template_name = "student_registration/cost_confirm_delete.html"
    success_url = reverse_lazy("student_registration:choices")


class WhyChoiceDeleteView(DeleteView):
    model = models.WhyChoice
    template_name = "student_registration/cost_confirm_delete.html"
    success_url = reverse_lazy("student_registration:choices")


class MonthlyCostCreateView(CreateView):
    form_class = forms.MonthlyCostForm
    template_name = "student_registration/monthly_cost_form.html"
    success_url = reverse_lazy("student_registration:cost-list")
    queryset = models.MonthlyCost.objects.all()


class RegistrationCostCreateView(CreateView):
    form_class = forms.RegistrationCostForm
    template_name = "student_registration/registration_cost_form.html"
    success_url = reverse_lazy("student_registration:cost-list")
    queryset = models.RegistrationCost.objects.all()


class MonthlyCostUpdateView(UpdateView):
    form_class = forms.MonthlyCostForm
    template_name = "student_registration/monthly_cost_form.html"
    success_url = reverse_lazy("student_registration:cost-list")
    queryset = models.MonthlyCost.objects.all()


class RegistrationCostUpdateView(UpdateView):
    form_class = forms.RegistrationCostForm
    template_name = "student_registration/registration_cost_form.html"
    success_url = reverse_lazy("student_registration:cost-list")
    queryset = models.RegistrationCost.objects.all()


class MonthlyCostDeleteView(DeleteView):
    model = models.MonthlyCost
    template_name = "student_registration/student_confirm_delete.html"
    success_url = reverse_lazy("student_registration:cost-list")


class RegistrationCostDeleteView(DeleteView):
    model = models.RegistrationCost
    template_name = "student_registration/student_confirm_delete.html"
    success_url = reverse_lazy("student_registration:cost-list")


def instructor_list(request):
    return render(
        request,
        template_name="student_registration/instructor_list.html",
        context={"instructors": models.Instructor.objects.all()},
    )


class InstructorCreate(CreateView):
    form_class = forms.InstructorForm
    template_name = "student_registration/instructor_form.html"
    success_url = reverse_lazy("student_registration:instructor-list")
    queryset = models.Instructor.objects.all()


class InstructorUpdate(UpdateView):
    form_class = forms.InstructorForm
    template_name = "student_registration/instructor_form.html"
    success_url = reverse_lazy("student_registration:instructor-list")
    queryset = models.Instructor.objects.all()


class InstructorDelete(DeleteView):
    model = models.Instructor
    template_name = "student_registration/student_confirm_delete.html"
    success_url = reverse_lazy("student_registration:instructor-list")
