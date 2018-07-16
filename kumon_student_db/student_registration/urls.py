from django.urls import path
from kumon_student_db.student_registration import views, api

app_name = "student_registration"
urlpatterns = [
    # Students Views
    path("students/", views.StudentList.as_view(), name="student-list"),
    path("students/create", views.StudentCreate.as_view(), name="student-add"),
    path("students/<int:pk>/", views.StudentUpdate.as_view(), name="student-update"),
    path(
        "students/<int:pk>/delete", views.StudentDelete.as_view(), name="student-delete"
    ),
    path("students/<int:pk>/printout", views.customer_copy, name="customer-copy"),
    # Cost Views
    path("costs/", views.cost_list, name="cost-list"),
    path(
        "costs/monthly_costs/create/",
        views.MonthlyCostCreateView.as_view(),
        name="monthly-cost-add",
    ),
    path(
        "costs/registration_costs/create/",
        views.RegistrationCostCreateView.as_view(),
        name="registration-cost-add",
    ),
    path(
        "costs/monthly_costs/<int:pk>/",
        views.MonthlyCostUpdateView.as_view(),
        name="monthly-cost-update",
    ),
    path(
        "costs/registration_costs/<int:pk>/",
        views.RegistrationCostUpdateView.as_view(),
        name="registration-cost-update",
    ),
    path(
        "costs/monthly_costs/<int:pk>/delete",
        views.MonthlyCostDeleteView.as_view(),
        name="monthly-cost-delete",
    ),
    path(
        "costs/registration_costs/<int:pk>/delete",
        views.RegistrationCostDeleteView.as_view(),
        name="registration-cost-delete",
    ),
    # Choices Views,
    path("choices/", views.choices, name="choices"),
    path(
        "choices/how/create",
        views.HowChoiceCreateView.as_view(),
        name="how-choice-create",
    ),
    path(
        "choices/why/create",
        views.WhyChoiceCreateView.as_view(),
        name="why-choice-create",
    ),
    path(
        "choices/how/<int:pk>/",
        views.HowChoiceUpdateView.as_view(),
        name="how-choice-update",
    ),
    path(
        "choices/how/<int:pk>/delete/",
        views.HowChoiceDeleteView.as_view(),
        name="how-choice-delete",
    ),
    path(
        "choices/why/<int:pk>/",
        views.WhyChoiceUpdateView.as_view(),
        name="why-choice-update",
    ),
    path(
        "choices/why/<int:pk>/delete/",
        views.WhyChoiceDeleteView.as_view(),
        name="why-choice-delete",
    ),
    # API
    path("api/cost_info", api.get_cost_info, name="cost-info"),
    path("api/how_choice_data", api.get_choice_data, name='choice-data'),
]
