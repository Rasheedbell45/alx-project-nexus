from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PollViewSet,
    OptionCreateView,
    VoteCreateView,
    PollListCreateView,
    PollDetailView,
    PollResultsView,
)

# Router for PollViewSet (list, create, retrieve, update, delete, vote, results)
router = DefaultRouter()
router.register(r'', PollViewSet, basename='poll')

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),

    # Additional custom endpoints (if needed)
    path('list-create/', PollListCreateView.as_view(), name='poll-list-create'),
    path('<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('<int:poll_id>/options/', OptionCreateView.as_view({'get': 'list', 'post': 'create'}), name='option-create'),
    path('options/<int:option_id>/vote/', VoteCreateView.as_view({'post': 'create'}), name='vote-create'),
    path('<int:poll_id>/vote/', VoteCreateView.as_view({'post': 'create'}), name='poll-vote'),
    path('<int:poll_id>/results/', PollResultsView.as_view(), name='poll-results'),
]
