from django.db import models
from utils.models import CommonFields, Choice
from user.models import CustomUser
# Create your models here.

class Category(CommonFields):
    category_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        db_table = 'category'
        

class Course(CommonFields):
    course_title = models.CharField(max_length=255)
    is_mandatory = models.BooleanField(null=True, blank= True, default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='course_category', null=True,blank=True)
    course_duration = models.DurationField(null=True, blank=True)
    no_of_assignee = models.PositiveIntegerField(null=True, blank=True)
    status = models.ForeignKey(Choice, on_delete=models.SET_NULL, related_name='course_status', null=True, blank=True, limit_choices_to={'choice_type': 'status'})
    
    def __str__(self):
        return f'{self.course_title} {self.course_duration}'
        
    class Meta:
        db_table = 'courses'
        
        
class Assignee(CommonFields):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='assignee_course', blank=True,null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='assignee_user')
    type = models.ForeignKey(Choice, on_delete=models.SET_NULL, related_name='assignee_type', limit_choices_to={'choice_type': 'assignee'}, null=True)
    designation = models.ForeignKey(Choice, on_delete=models.SET_NULL, related_name='assignee_designation',limit_choices_to={'choice_type': 'designation'}, blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    grade = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} and designation is {self.designation}'

    class Meta:
        db_table = 'assignees'
    

class Module(CommonFields):
    module_number = models.IntegerField()
    module_name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_module')
    
    def __str__(self):
        return f'{self.module_name} {self.module_number}'
        
    class Meta:
        db_table = 'modules'
        ordering = ["module_number"]
        
            
class Lesson(CommonFields):
    lesson_number = models.IntegerField()
    lesson_name = models.CharField(max_length=255)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module_lesson')
    lesson_duration = models.DurationField(null=True, blank=True)
    lesson_description = models.TextField(null=True, blank=True)
    media = models.FileField(upload_to='media/lesson_files', null=True, blank=True)
    
    def __str__(self):
        return f'{self.lesson_number} {self.lesson_name}'
    class Meta:
        db_table = 'lessons'
        ordering = ["lesson_number"]
        
        
        
class Question(CommonFields):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name= 'module_question')
    question = models.CharField(max_length=255)
    type = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'choice_type': 'answer'}, related_name='question_type')
    
    def __str__(self):
        return self.question
    class Meta:
        db_table = 'questions'
        
        
class QuestionOptions(CommonFields):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='question_options_question',
    )
    options = models.CharField(max_length=255,)

    def __str__(self):
        return f'{self.options}'

    class Meta:
        db_table = 'question_options'
        unique_together = ('question', 'options')
        
class Answer(CommonFields):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer')
    answer = models.CharField(max_length=255, null=True, blank=True)
    is_correct = models.BooleanField(null=True, blank=True, default=False)
    
    def __str__(self):
        return f'{self.answer} {self.is_correct}'
    
    class Meta:
        db_table = 'answers'
        
        

        
    

    
    
    
    
    
