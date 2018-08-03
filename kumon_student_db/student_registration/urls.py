from django.urls import path
from kumon_student_db.student_registration import views, api

app_name = "student_registration"
urlpatterns = [
    # Student Application Views
    path(
        "student_applications/",
        views.StudentApplicationList.as_view(),
        name="student-application-list",
    ),
    path(
        "student_applications/create",
        views.StudentApplicationCreate.as_view(),
        name="student-application-create",
    ),
    path(
        "student_applications/<int:pk>/",
        views.StudentApplicationUpdate.as_view(),
        name="student-application-update",
    ),
    path(
        "student_applications/<int:pk>/delete",
        views.StudentApplicationDelete.as_view(),
        name="student-application-delete",
    ),
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
    # Instructor Views
    path("instructors/", views.instructor_list, name="instructor-list"),
    path(
        "instructors/create", views.InstructorCreate.as_view(), name="instructor-create"
    ),
    path(
        "instructors/<int:pk>",
        views.InstructorUpdate.as_view(),
        name="instructor-update",
    ),
    path(
        "instructors/<int:pk>/delete",
        views.InstructorDelete.as_view(),
        name="instructor-delete",
    ),
    # API
    path("api/cost_info", api.get_cost_info, name="cost-info"),
    path("api/how_choice_data/", api.how_choice_data, name="choice-data"),
    path("api/why_choice_data/", api.why_choice_data, name="choice-data"),
    path("api/students_csv/", api.student_csv, name="student-csv"),
]
