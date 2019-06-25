from django.db import models
from django.utils import timezone

class Category(models.Model):
    category = models.CharField(max_length=200)
    def __str__(self):
        return self.category

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    total_polled = models.IntegerField(default=0)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    percentage = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

