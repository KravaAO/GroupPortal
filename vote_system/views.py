from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Voting, Choice, VoteRecord
from django.urls import reverse_lazy
from .forms import VotingForm
# Create your views here.


class VotingDetailView(LoginRequiredMixin, DetailView):
    model = Voting
    template_name = 'vote_system/voting_detail.html'
    context_object_name = 'voting'

    def post(self, request, *args, **kwargs):
        voting = self.get_object()
        choice_id = request.POST.get('choice')

        if choice_id:
            choice = get_object_or_404(Choice, id=choice_id)
            vote, created = VoteRecord.objects.update_or_create(
                user=request.user,
                voting=voting,
                defaults={'choice': choice}
            )
            return redirect('vote_system:voting_list')
        return self.get(request, *args, **kwargs)



class VotingListView(ListView):
    model = Voting
    template_name = 'vote_system/voting_list.html'
    context_object_name = 'votings'

class VotingCreateView(LoginRequiredMixin, CreateView):
    model = Voting
    form_class = VotingForm
    template_name = 'vote_system/voting_form.html'
    success_url = reverse_lazy('vote_system:voting_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        choices = self.request.POST.getlist('choices_text')
        for text in choices:
            if text.strip():
                Choice.objects.create(voting=self.object,choice_text=text)
        return response

class VotingDeleteView(LoginRequiredMixin,DeleteView):
    model = Voting
    template_name = 'vote_system/voting_confirm_delete.html'
    success_url = reverse_lazy('vote_system:voting_list')

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


