from rest_framework import generics, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import F
from django.shortcuts import get_object_or_404
from .models import Poll, Option, Vote
from .serializers import PollSerializer, OptionSerializer, VoteSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.utils import timezone
from django.db import transaction, IntegrityError

class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class PollDetailView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class OptionCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, poll_id):
        poll = get_object_or_404(Poll, id=poll_id)
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(poll=poll)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VoteCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, option_id):
        option = get_object_or_404(Option, id=option_id)
        # prevent double voting
        if Vote.objects.filter(option=option, voter=request.user).exists():
            return Response({"error": "You already voted on this option."},
                            status=status.HTTP_400_BAD_REQUEST)
        vote = Vote.objects.create(option=option, voter=request.user)
        serializer = VoteSerializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow write only to the poll creator; read to all (or staff)."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and (request.user == obj.created_by or request.user.is_staff)

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.prefetch_related('options').all().order_by('-created_at')
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        """
        POST /api/polls/{pk}/vote/
        payload: { "option_id": <id> }
        """
        poll = self.get_object()
        if poll.expires_at and poll.expires_at < timezone.now():
            return Response({"detail": "Poll has expired."}, status=status.HTTP_400_BAD_REQUEST)

        option_id = request.data.get("option_id")
        if not option_id:
            return Response({"detail": "option_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        option = get_object_or_404(Option, pk=option_id, poll=poll)

        # Prevent duplicate voting (db unique constraint covers it too)
        existing = Vote.objects.filter(poll=poll, voter=request.user).first()
        if existing:
            return Response({"detail": "You have already voted in this poll."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Create vote
                Vote.objects.create(poll=poll, option=option, voter=request.user)
                # Atomically increment denormalized counter (if you maintain one), or update via F expression for safety
                # If you maintain votes_count on Option, do: Option.objects.filter(pk=option.pk).update(votes_count=F('votes_count')+1)
                # Here we rely on DB for real counts but show atomic update example:
                # Option.objects.filter(pk=option.pk).update(votes_count=F('votes_count') + 1)
        except IntegrityError:
            return Response({"detail": "Duplicate vote detected."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Vote recorded."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def results(self, request, pk=None):
        """
        GET /api/polls/{pk}/results/
        returns options with votes_count
        """
        poll = self.get_object()
        options = poll.options.all()
        # Efficient aggregation: annotate counts if needed, but OptionSerializer votes_count uses .votes.count
        serializer = OptionSerializer(options, many=True)
        return Response({
            "poll_id": poll.id,
            "question": poll.question,
            "options": serializer.data
        })
