from django.urls import path
from kumon_student_db.student_registration.views import StudentList

app_name = "student_registration"
urlpatterns = [
    path("students/", StudentList.as_view()),
]
