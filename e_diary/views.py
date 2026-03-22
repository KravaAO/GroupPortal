from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
from e_diary.forms import add_grade  
from e_diary.models import Diary,Grade
from django.forms import Form
from django.contrib.auth.mixins import LoginRequiredMixin
class your_grades(View,LoginRequiredMixin):
    def get(self,request):
        diaryy = Diary.objects.get(user_profile = request.user)
        all_grades = diaryy.grades.all()
        return render(request,"your_diary.html",{"grades" : all_grades})
    def post(self,request):
        return render(request,"your_diary.html")
class teacher_crud(View):
    def get():
        ...
