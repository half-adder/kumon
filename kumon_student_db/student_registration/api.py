from dateutil import parser
from decimal import Decimal

from django.http import HttpResponse, JsonResponse

from kumon_student_db.student_registration import utils, models


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


def get_choice_data(request):
    how_choice_counts = utils.get_choice_counts('how')
    why_choice_counts = utils.get_choice_counts('why')
    return JsonResponse({
        'how_choice_counts': how_choice_counts,
        'why_choice_counts': why_choice_counts
    })


def how_choice_data(request):
    return JsonResponse(utils.get_choice_counts('how'))


def why_choice_data(request):
    return JsonResponse(utils.get_choice_counts('why'))


def student_csv(request):
    return utils.students_csv(request, models.Student.objects.all())
