from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.http import JsonResponse, HttpResponse

from dateutil import parser

from kumon_student_db.student_registration import models, forms, utils


class StudentList(ListView):
    model = models.Student


class StudentDetail(DetailView):
    model = models.Student

    def get_object(self, queryset=models.Student.objects.all()):
        return super().get_object()


class StudentForm(FormView):
    template_name = "student_registration/student_form.html"
    form_class = forms.StudentForm
    success_url = "/"


class ParentList(ListView):
    model = models.Parent


class ParentDetail(DetailView):
    model = models.Parent

    def get_object(self, queryset=models.Parent.objects.all()):
        return super().get_object()


# API Functions
def validate_request(request, allowed_methods, required_params):
    """
    TODO: docs
    TODO: tests
    :param request:
    :return:
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
    :param request:
    :return:
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
    :param request:
    :return:
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

    monthly_cost = models.MonthlyCost.get_cost_for(start_date)
    registration_base_cost = models.RegistrationCost.get_cost_for(start_date)

    response = {
        "monthly_cost": monthly_cost,
        "registration_base_cost": registration_base_cost,
        "prorated_cost": utils.prorated_cost(start_date, monthly_cost),
        "total_cost": utils.total_cost(
            start_date, monthly_cost, registration_base_cost, n_subjects
        ),
    }

    return JsonResponse(response)
