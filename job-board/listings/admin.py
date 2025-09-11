# listings/admin.py
from django.contrib import admin
from .models import Category, Job, Application

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ["name"]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "job_type", "is_active", "created_at")
    search_fields = ["title", "company", "location"]
    list_filter = ("job_type", "category", "is_active")
    prepopulated_fields = {"slug": ("title", "company")}


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "applicant", "created_at")
    search_fields = ["applicant__username", "job__title"]
