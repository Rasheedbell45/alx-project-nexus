from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction, IntegrityError
from django.db.models import Count

from .models import Poll, Option, Vote
from .serializers import PollSerializer, OptionSerializer, VoteSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: only poll creator or staff can edit/delete.
    Others get read-only access.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.created_by or request.user.is_staff


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.prefetch_related("options").all().order_by("-created_at")
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        poll = serializer.save(created_by=self.request.user)
        options_data = self.request.data.get("options", [])
        for option in options_data:
            if option.get("text"):
                Option.objects.create(poll=poll, text=option["text"])

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def vote(self, request, pk=None):
        poll = self.get_object()
        if poll.expires_at and poll.expires_at < timezone.now():
            return Response({"detail": "Poll has expired."}, status=status.HTTP_400_BAD_REQUEST)

        option_id = request.data.get("option_id")
        if not option_id:
            return Response({"detail": "option_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        option = get_object_or_404(Option, pk=option_id, poll=poll)

        if Vote.objects.filter(poll=poll, voter=request.user).exists():
            return Response({"detail": "You have already voted in this poll."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                Vote.objects.create(poll=poll, option=option, voter=request.user)
        except IntegrityError:
            return Response({"detail": "Duplicate vote detected."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Vote recorded."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"], permission_classes=[permissions.AllowAny])
    def results(self, request, pk=None):
        poll = self.get_object()
        options = poll.options.annotate(votes_count=Count("votes"))
        serializer = OptionSerializer(options, many=True)
        return Response({
            "poll_id": poll.id,
            "question": poll.question,
            "options": serializer.data
        })


class OptionCreateView(viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Option.objects.filter(poll_id=self.kwargs.get("poll_id"))

    def perform_create(self, serializer):
        poll = get_object_or_404(Poll, id=self.kwargs.get("poll_id"))
        serializer.save(poll=poll)


class VoteCreateView(viewsets.ModelViewSet):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(voter=self.request.user)

    def create(self, request, *args, **kwargs):
        option_id = request.data.get("option_id")
        if not option_id:
            return Response({"detail": "option_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        option = get_object_or_404(Option, id=option_id)
        poll = option.poll

        if poll.expires_at and poll.expires_at < timezone.now():
            return Response({"detail": "Poll has expired."}, status=status.HTTP_400_BAD_REQUEST)

        if Vote.objects.filter(poll=poll, voter=request.user).exists():
            return Response({"detail": "You have already voted in this poll."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                vote = Vote.objects.create(poll=poll, option=option, voter=request.user)
        except IntegrityError:
            return Response({"detail": "Duplicate vote detected."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollResultsView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()

    def retrieve(self, request, *args, **kwargs):
        poll = self.get_object()
        options = poll.options.annotate(votes_count=Count('votes'))
        serializer = OptionSerializer(options, many=True)
        return Response({
            "poll_id": poll.id,
            "question": poll.question,
            "options": serializer.data
        })
