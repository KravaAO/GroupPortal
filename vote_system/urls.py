from django.urls import path
from .views import VotingListView, VotingDetailView, VotingCreateView, VotingDeleteView

app_name = 'vote_system'

urlpatterns = [
    path('create/', VotingCreateView.as_view(), name='voting_create'),
    path('', VotingListView.as_view(), name='voting_list'),
    path('<int:pk>/', VotingDetailView.as_view(),name='voting_detail'),
    path('<int:pk>/delete/',VotingDeleteView.as_view(),name='voting_delete'),
]