from django.contrib.auth.models import User
from django.shortcuts import render
from django.views import View
#from forms import add_grade
from .models import Diary,Grade
class Create_grade(View):
    def post():
        all_grades = Diary.objects.get(user_profile = User.get_username())
        
