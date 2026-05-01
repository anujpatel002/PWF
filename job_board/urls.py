from django.urls import path
from . import views

app_name = 'job_board'

urlpatterns = [
    # ── HTML Views ────────────────────────────────────────────────────────────
    path('jobs/',             views.job_list,   name='job_list'),
    path('jobs/new/',         views.job_create, name='job_create'),
    path('jobs/<int:pk>/',    views.job_detail, name='job_detail'),

    # ── REST API Endpoints ────────────────────────────────────────────────────
    # Companies
    path('api/companies/',           views.CompanyListCreateView.as_view(),         name='company_list_create'),
    path('api/companies/<int:pk>/',  views.CompanyRetrieveUpdateDestroyView.as_view(), name='company_detail'),

    # Job Posts (full CRUD via API — includes INSERT and DELETE)
    path('api/jobs/',           views.JobPostListCreateView.as_view(),          name='job_api_list_create'),
    path('api/jobs/<int:pk>/',  views.JobPostRetrieveUpdateDestroyView.as_view(), name='job_api_detail'),
]
