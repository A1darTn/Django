from django.contrib import admin

from .models import Student, Teachers


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Teachers)
class TeacherAdmin(admin.ModelAdmin):
    pass
