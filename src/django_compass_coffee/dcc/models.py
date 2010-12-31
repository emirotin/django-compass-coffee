from django.db import models

class Poll(models.Model):
    """The class represents the poll instance"""
    question = models.TextField(max_length=500)
    
class PollAnswer(models.Model):
    """The class represents the poll answer option"""
    answer = models.TextField(max_length=500)
    poll = models.ForeignKey(Poll)
    
class RegisteredAnswer(models.Model):
    """The class represents a user answer registered"""
    answer = models.ForeignKey(PollAnswer)
    timestamp = models.DateTimeField(auto_now_add=True)