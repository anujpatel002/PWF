from django.contrib import admin
from .models import Company, JobPost


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display  = ('name', 'industry', 'location', 'website')
    list_filter   = ('industry', 'location')
    search_fields = ('name', 'industry')


@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'company', 'location', 'salary', 'posted_date')
    list_filter   = ('company', 'location')
    search_fields = ('title', 'description')
    raw_id_fields = ('company',)
    ordering      = ('-posted_date',)
