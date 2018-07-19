from django.contrib import admin
from kumon_student_db.student_registration import models

# Register your models here.
admin.site.register(models.MonthlyCost)
admin.site.register(models.RegistrationCost)
admin.site.register(models.WhyChoice)
admin.site.register(models.HowChoice)
admin.site.register(models.Parent)
admin.site.register(models.Student)
admin.site.register(models.Instructor)
