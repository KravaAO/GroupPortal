from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from e_diary.forms import add_grade  
from e_diary.models import Diary,Grade
from django.forms import Form
from django.contrib.auth.mixins import LoginRequiredMixin
class your_grades(LoginRequiredMixin,ListView):
    model = Grade
    template_name = "your_diary.html"
    context_object_name = "grades" 
    def get_queryset(self,request):
        diaryy = Diary.objects.get(diary_connection = request.user)
        all_grades = diaryy.grades.all()
        return all_grades
    def post(self,request):
        return render(request,"your_diary.html")
class Note_create_view(LoginRequiredMixin,View):
    template_name = "crud.html"
    model = Grade
    fields = ["grade","messege"]
    def form_valid():
        diary = Diary.objects.get()
        form.instance.diary = diary
        return super().form_valid(form) 
