from django.urls import path
from kumon_student_db.student_registration import views

app_name = "student_registration"
urlpatterns = [
    path("students/", views.StudentList.as_view(), name='student-list'),
    path("students/<int:pk>/", views.StudentDetail.as_view(), name='student-detail'),
]
