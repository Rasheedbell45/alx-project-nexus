from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import PollViewSet, OptionCreateView, VoteCreateView

router = DefaultRouter()
router.register(r'', PollViewSet, basename='poll')

urlpatterns = router.urls + [
    # Options for a poll
    path('<int:poll_id>/options/', OptionCreateView.as_view({'get': 'list', 'post': 'create'}), name='option-create'),
    
    # Vote on a specific option
    path('options/<int:option_id>/vote/', VoteCreateView.as_view({'post': 'create'}), name='vote-create'),

    # Vote on a poll
    path('<int:poll_id>/vote/', VoteCreateView.as_view({'post': 'create'}), name='poll-vote'),
]
