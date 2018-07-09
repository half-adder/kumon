from django.urls import path
from kumon_student_db.student_registration import views

app_name = "student_registration"
urlpatterns = [
    path("students/", views.StudentList.as_view(), name="student-list"),
    path("students/create", views.StudentCreate.as_view(), name="student-add"),
    path("students/<int:pk>/", views.StudentUpdate.as_view(), name="student-update"),
    path("students/<int:pk>/delete", views.StudentDelete.as_view(), name="student-delete"),
    path("api/cost_info", views.get_cost_info, name="cost-info"),
]
