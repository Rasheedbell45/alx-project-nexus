# listings/views.py
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Job, Application
from .serializers import CategorySerializer, JobSerializer, ApplicationSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated

# Custom permission: Admins / staff can edit; others read-only
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.select_related("category", "posted_by").all()
    serializer_class = JobSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category__slug", "location", "job_type", "is_active"]
    search_fields = ["title", "company", "description"]
    ordering_fields = ["created_at", "company", "title"]

    def perform_create(self, serializer):
        # posted_by set to request.user for admin or staff
        serializer.save(posted_by=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def apply(self, request, pk=None):
        """Endpoint for a user to apply for a job (POST /jobs/{pk}/apply/)"""
        job = self.get_object()
        serializer = ApplicationSerializer(data={**request.data, "job_id": job.id}, context={"request": request})
        if serializer.is_valid():
            # set applicant
            serializer.save(applicant=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.select_related("job", "applicant").all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users see only their applications; admins can see all
        user = self.request.user
        if user.is_staff:
            return Application.objects.select_related("job", "applicant").all()
        return Application.objects.filter(applicant=user).select_related("job")
