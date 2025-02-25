from django.db import models
from .choices import CHOICE_TYPE

# Create your models here.
class CommonFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
    
    
class Choice(CommonFields):
    choice_name = models.CharField(max_length=255)     # male, female
    choice_type = models.CharField(max_length=255, choices=CHOICE_TYPE)       # gender
    
    def __str__(self):
        return self.choice_name
    
    class Meta:
        db_table = 'choices'
        unique_together = ('choice_name', 'choice_type',)
