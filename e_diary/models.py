from django.db import models
# Create your models here.
class Diary(models.Model):
    """
        модель щоденника 
         
         -через grades прописуеться звязок між таблицями оцінок та таблицею щоденника
    """
    user_profile = models.OneToOneField()
    grades = models.ForeignKey(Grade,on_delete=models.CASCADE)


class Grade(models.Model):
    """
        Модель для привязки запису оцінки до користувача
    """
    user_profile = models.OneToOneField(on_delete=models.CASCADE)#TODO:поміняти назву якось
    grade = models.SmallIntegerField()


