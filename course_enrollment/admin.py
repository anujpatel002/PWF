from django.contrib import admin
from .models import Course, Student


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display  = ('name', 'duration')
    search_fields = ('name', 'description')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display   = ('name', 'email', 'contact')
    search_fields  = ('name', 'email')
    # filter_horizontal renders M2M as a dual-list widget in the admin
    filter_horizontal = ('courses',)
