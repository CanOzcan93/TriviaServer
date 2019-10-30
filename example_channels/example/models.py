from django.conf import settings
from django.db import models


class LoggedInUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='logged_in_user')

class Person(models.Model):
    name = models.CharField(max_length=75)
    wild_card = models.IntegerField()

    def __str__(self):
        return self.name + ": " + str(self.wild_card) + "\n"

class Game(models.Model):
    persons = models.ManyToManyField(Person,through="Membership")
    is_active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    room = models.CharField(max_length=30,default="")
    currentQuestion = models.IntegerField(default=1)

class Membership(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    isFailed = models.BooleanField(default=False)
    used_wildcard = models.BooleanField(default=False)
    answer_one = models.CharField(max_length=100,default="")
    answer_two = models.CharField(max_length=100,default="")
    answer_three = models.CharField(max_length=100,default="")
    answer_four = models.CharField(max_length=100,default="")
    answer_five = models.CharField(max_length=100,default="")
    answer_six = models.CharField(max_length=100,default="")
    answer_seven = models.CharField(max_length=100,default="")
    answer_eight = models.CharField(max_length=100,default="")
    answer_nine = models.CharField(max_length=100,default="")
    answer_ten = models.CharField(max_length=100,default="")
    answer_eleven = models.CharField(max_length=100,default="")
    answer_twelwe = models.CharField(max_length=100,default="")

class Question(models.Model):
    question = models.CharField(max_length = 500,default="")
    correct_answer = models.CharField(max_length = 100,default="")
    wrong_answer_one = models.CharField(max_length = 100,default="")
    wrong_answer_two = models.CharField(max_length = 100,default="")
    wrong_answer_three = models.CharField(max_length = 100,default="")
    
