from django.urls import path
from . import views

app_name = 'vote_system'

urlpatterns = [
    path('create/', views.VotingCreateView.as_view(), name='voting_create'),
    path('', views.VotingListView.as_view(), name='voting_list'),
    path('<int:pk>/', views.VotingDetailView.as_view(),name='voting_detail'),
    path('<int:pk>/delete/',views.VotingDeleteView.as_view(),name='voting_delete'),
]