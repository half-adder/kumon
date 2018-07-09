from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.http import JsonResponse, HttpResponse

from dateutil import parser
from decimal import Decimal

from kumon_student_db.student_registration import models, forms, utils


# Template Views
class StudentList(ListView):
    model = models.Student


class StudentCreate(CreateView):
    form_class = forms.StudentForm
    template_name = "student_registration/student_form_crispy.html"
    success_url = reverse_lazy("student_registration:student-list")

    def get_queryset(self):
        return models.Student.objects.all()


class StudentUpdate(UpdateView):
    form_class = forms.StudentForm
    template_name = "student_registration/student_form_crispy.html"
    success_url = reverse_lazy("student_registration:student-list")
    queryset = models.Student.objects.all()


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


# API Views
def validate_request(request, allowed_methods, required_params):
    """
    TODO: docs
    TODO: tests
    """
    if request.method not in allowed_methods:
        return HttpResponse("Only GET is allowed for this method", status=500)
    try:
        assert all(param in request.GET for param in required_params)
    except AssertionError as e:
        return HttpResponse(e, status=500)


def parse_start_date_or_error(request):
    """
    TODO: docs
    TODO: tests
    """
    try:
        start_date_str = request.GET["start_date"]
        return parser.isoparse(start_date_str).date()
    except Exception as e:  # TODO: more specific
        return HttpResponse(e, status=500)


def parse_n_subjects_or_error(request):
    """
    TODO: docs
    TODO: tests
    """
    try:
        return int(request.GET["n_subjects"])
    except Exception as e:  # TODO: more specific
        return HttpResponse(e, status=500)


def get_cost_info(request):
    validate_request(
        request, ["GET"], ["start_date", "n_subjects", "registration_discount"]
    )

    start_date = parse_start_date_or_error(request)
    n_subjects = parse_n_subjects_or_error(request)
    registration_discount = Decimal(request.GET["registration_discount"])

    registration_base_cost = models.RegistrationCost.get_cost_for(start_date)
    registration_cost = float(
        (100 - registration_discount) * registration_base_cost / 100
    )
    monthly_cost = models.MonthlyCost.get_cost_for(start_date)

    response = {
        "monthly_cost": monthly_cost,
        "registration_cost": registration_cost,
        "prorated_cost": utils.prorated_cost(start_date, monthly_cost),
        "total_cost": utils.total_cost(
            start_date, monthly_cost, registration_cost, n_subjects
        ),
    }

    return JsonResponse(response)
