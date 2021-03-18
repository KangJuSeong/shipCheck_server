from django.db import models
from Accounts.models import Account


class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    types = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    writer = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return "{0}({1}) - {2}".format(self.title, self.id, self.writer)


class Answer(models.Model):
    answer = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    q_id = models.OneToOneField(Question, on_delete=models.CASCADE)


class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    types = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
