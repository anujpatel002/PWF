from django.urls import path
from . import views

app_name = 'course_enrollment'

urlpatterns = [
    path('add/',                         views.add_course,      name='add_course'),
    path('',                             views.course_list,     name='course_list'),
    path('<int:course_id>/enroll/',      views.enroll_student,  name='add_enrollment'),
    path('<int:course_id>/students/',    views.student_course,  name='student_course'),
]
