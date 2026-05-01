from rest_framework import generics
from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, JobPost
from .serializers import CompanySerializer, JobPostSerializer
from .forms import JobPostForm

# ── CHEATSHEET: DRF Generic Class-Based Views (API) ──────────────────────────
# ListCreateAPIView          → GET (list) + POST (create)
# RetrieveUpdateDestroyAPIView → GET (detail) + PUT/PATCH (update) + DELETE
# These replace manually writing list/create/retrieve/update/destroy FBVs.
# queryset     → the base queryset the view operates on
# serializer_class → the serializer used for validation and serialization
# ─────────────────────────────────────────────────────────────────────────────

# ── Company API ──────────────────────────────────────────────────────────────

class CompanyListCreateView(generics.ListCreateAPIView):
    """GET /api/companies/  →  list all; POST  →  create new company."""
    queryset         = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH /api/companies/<pk>/  or  DELETE to remove a company."""
    queryset         = Company.objects.all()
    serializer_class = CompanySerializer


# ── JobPost API ───────────────────────────────────────────────────────────────

class JobPostListCreateView(generics.ListCreateAPIView):
    """GET /api/jobs/  →  list all jobs; POST  →  create a new job post."""
    queryset         = JobPost.objects.select_related('company').all()
    serializer_class = JobPostSerializer


class JobPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """GET /api/jobs/<pk>/  →  detail; PUT/PATCH  →  update; DELETE  →  remove."""
    queryset         = JobPost.objects.select_related('company').all()
    serializer_class = JobPostSerializer


# ── HTML / FBV Views ─────────────────────────────────────────────────────────

def job_create(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_board:job_list')
    else:
        form = JobPostForm()
    return render(request, 'jobs/job_form.html', {'form': form})


def job_list(request):
    jobs      = JobPost.objects.all()
    companies = Company.objects.all()

    # ── CHEATSHEET: QuerySet Filtering via GET params ─────────────────────
    # request.GET.get('key') reads ?key=value from the URL query string
    company_id = request.GET.get('company')
    if company_id:
        jobs = jobs.filter(company_id=company_id)  # chain .filter() calls
    # ──────────────────────────────────────────────────────────────────────

    return render(request, 'jobs/job_list.html', {
        'jobs':      jobs,
        'companies': companies,
    })


def job_detail(request, pk):
    job = get_object_or_404(JobPost, pk=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})
