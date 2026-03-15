from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from e_diary.models import Diary


class your_grades(LoginRequiredMixin, View):
    template_name = "your_diary.html"

    def get(self, request):
        diary, _ = Diary.objects.get_or_create(user_profile=request.user)
        grades = diary.grades.all()
        return render(request, self.template_name, {"grades": grades})
