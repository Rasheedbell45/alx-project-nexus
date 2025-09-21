from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PollListCreateView, PollDetailView, OptionCreateView, VoteCreateView, PollViewSet

router = DefaultRouter()
router.register(r'', PollViewSet, basename='poll')

urlpatterns = router.urls
urlpatterns = [
    path('', PollListCreateView.as_view(), name='poll-list-create'),
    path('<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('<int:poll_id>/options/', OptionCreateView.as_view(), name='option-create'),

    # Voting (supports both styles)
    path('options/<int:option_id>/vote/', VoteCreateView.as_view(), name='vote-create'),
    path('<int:poll_id>/vote/', VoteCreateView.as_view(), name='poll-vote'),

    # Results
    path('<int:poll_id>/results/', PollResultsView.as_view(), name='poll-results'),
]
