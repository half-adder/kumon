from django import forms
from kumon_student_db.student_registration import models


class StudentForm(forms.ModelForm):
    class Meta:
        model = models.Student
        fields = '__all__'
