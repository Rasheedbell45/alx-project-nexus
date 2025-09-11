# listings/models.py
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Job(models.Model):
    FULL_TIME = "FT"
    PART_TIME = "PT"
    CONTRACT = "CT"
    INTERNSHIP = "IN"
    TYPE_CHOICES = [
        (FULL_TIME, "Full-time"),
        (PART_TIME, "Part-time"),
        (CONTRACT, "Contract"),
        (INTERNSHIP, "Internship"),
    ]

    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    company = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name="jobs", on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=255, db_index=True)  # simple location string; for geo use PostGIS
    job_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=FULL_TIME, db_index=True)
    description = models.TextField()
    search_vector = SearchVectorField(null=True, blank=True)  # for PostgreSQL full-text
    is_active = models.BooleanField(default=True, db_index=True)
    posted_by = models.ForeignKey(User, related_name="posted_jobs", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["location"]),
            models.Index(fields=["job_type"]),
            GinIndex(fields=["description"], name="job_description_gin"),  # optional GIN index for full-text
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.title}-{self.company}")
            self.slug = base[:300]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} @ {self.company}"


class Application(models.Model):
    job = models.ForeignKey(Job, related_name="applications", on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, related_name="applications", on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("job", "applicant")  # single application per user per job

    def __str__(self):
        return f"Application by {self.applicant} to {self.job}"
