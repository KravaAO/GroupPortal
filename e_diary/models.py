from django.db import models 
from django.contrib.auth.models import User  
# Create your models here.
class Diary(models.Model):
    """
        модель щоденника 
         
         -через grades прописуеться звязок між таблицями оцінок та таблицею щоденника
    """
    user_profile = models.OneToOneField(User,on_delete= models.CASCADE)
    #username = User.get_username()
    
class Grade(models.Model):
    """
        Модель для привязки запису оцінки до користувача
        включае в себе поле для оцінки (grade) та для зауваження вчителя(messege) 
    """
    user_profile = models.ForeignKey(Diary,on_delete=models.CASCADE,related_name="grades")
    grade = models.SmallIntegerField()
    messege = models.TextField(default = "")
    def __str__(self):
        return str(self.user_profile)

