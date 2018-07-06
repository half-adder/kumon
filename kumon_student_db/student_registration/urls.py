from django.urls import path
from kumon_student_db.student_registration import views

app_name = "student_registration"
urlpatterns = [
    path("students/", views.StudentList.as_view(), name='student-list'),
    path("students/<int:pk>/", views.StudentDetail.as_view(), name='student-detail'),
    path("students/create", views.StudentForm.as_view(), name='student-form'),

    path("parents/", views.ParentList.as_view(), name='parent-list'),
    path("parents/<int:pk>/", views.ParentDetail.as_view(), name='parent-detail'),

    path("api/cost_info", views.get_cost_info, name='prorated-cost')
]
