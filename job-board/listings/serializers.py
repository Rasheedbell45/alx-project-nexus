# listings/serializers.py
from rest_framework import serializers
from .models import Category, Job, Application

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class JobSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(write_only=True, source="category", queryset=Category.objects.all())
    posted_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Job
        fields = [
            "id", "title", "slug", "company", "category", "category_id", "location",
            "job_type", "description", "is_active", "posted_by", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "slug", "posted_by", "created_at", "updated_at"]


class ApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.StringRelatedField(read_only=True)
    job = JobSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Job.objects.all(), source="job")

    class Meta:
        model = Application
        fields = ["id", "job", "job_id", "applicant", "resume", "cover_letter", "created_at"]
        read_only_fields = ["id", "applicant", "created_at"]
