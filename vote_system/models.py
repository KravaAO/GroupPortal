from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Voting(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок голосування")
    description = models.TextField(verbose_name='Опис')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата Створення')
    is_active = models.BooleanField(default=True, verbose_name='Активне')

    def __str__(self):
        return self.title

class Choice(models.Model):
    voting = models.ForeignKey(Voting, related_name='choices')
    choice_text = models.CharField(max_length=200, verbose_name='текст варіанту')
    votes_count = models.IntegerField(default=0, verbose_name='Кількість голосів')

    def __str__(self):
        return f"{self.choice_text}({self.voting.title})"
                
class VoteRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted_ad = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'voting')

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name='Текст коментаря')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Коментар від {self.author.username}"


class Repost(model.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE, related_name='reposts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'voting')

