from rest_framework import serializers
from .models import Company, JobPost

# ── CHEATSHEET: DRF ModelSerializer ──────────────────────────────────────────
# ModelSerializer auto-generates fields from the Model.
# fields = '__all__'      → include every field
# fields = ['id', 'name'] → whitelist specific fields
# read_only_fields        → fields shown in response but not accepted in POST/PUT
# ─────────────────────────────────────────────────────────────────────────────

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Company
        fields = '__all__'


class JobPostSerializer(serializers.ModelSerializer):
    # Nested read-only: shows company name in GET responses
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model            = JobPost
        fields           = ['id', 'title', 'description', 'location', 'salary',
                            'company', 'company_name', 'posted_date']
        read_only_fields = ['posted_date']
