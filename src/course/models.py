from django.db import models
from utils.models import CommonFields, Choice
from user.models import CustomUser

class Category(CommonFields):
    """
    Represents a category that groups courses.
    Attributes:
        category_name: The name of the category.(training, learning)
    Methods:
        __str__(): Returns the category name as a string.
    Meta:
        db_table (str): Specifies the database table name as 'category'.
    """
    category_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        db_table = 'category'  
        

class Course(CommonFields):
    """
    Represents a courses.
    Attributes:
        course_title: The title of the course.
        is_mandatory: Indicates whether the course is mandatory.
        category: The category to which the course belongs.
        status: The status of the course, filtered by choice type "status".(active/inactive)
    Methods:
        __str__(): Returns a string representation of the course, including title.
    Meta:
        db_table (str): Specifies the database table name as 'courses'.
    """
    course_title = models.CharField(max_length=255)
    is_mandatory = models.BooleanField(null=True, blank= True, default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='course_category', null=True,blank=True)
    status = models.ForeignKey(Choice, on_delete=models.SET_NULL, related_name='course_status', null=True, blank=True, limit_choices_to={'choice_type': 'status'})
    
    def __str__(self):
        return f'{self.course_title}'
        
    class Meta:
        db_table = 'courses'
        

class Module(CommonFields):
    """
    Represents a module within a course.
    Attributes:
        module_number: The sequential number of the module.
        module_name: The name of the module.
        course: The course to which this module belongs.
    Methods:
        __str__(): Returns a string representation of the module, including its name and number.
    Meta:
        db_table : Specifies the database table name as 'modules'.
        ordering : Orders modules by 'module_number' in ascending order.
    """

    module_number = models.IntegerField()
    module_name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_module')
    
    def __str__(self):
        return f'{self.module_name} {self.module_number}'
        
    class Meta:
        db_table = 'modules'
        ordering = ["module_number"]
        
            
class Lesson(CommonFields):
    """
    Represents a lesson within a module.
    Attributes:
        lesson_number: The sequential number of the lesson.
        lesson_name: The name of the lesson.
        module: The module to which this lesson belongs.
        lesson_duration: The estimated duration of the lesson.
        lesson_description: A detailed description of the lesson.
        media: A URL linking to lesson media (e.g., video, document), stored in the cloud.
    Methods:
        __str__(): Returns a string representation of the lesson, including its number and name.
    Meta:
        db_table : Specifies the database table name as 'lessons'.
        ordering : Orders lessons by 'lesson_number' in ascending order.
    """
    lesson_number = models.IntegerField()
    lesson_name = models.CharField(max_length=255)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='module_lesson')
    lesson_duration = models.DurationField(null=True, blank=True)
    lesson_description = models.TextField(null=True, blank=True)
    media = models.URLField(max_length=250, null=True, blank=True)  #url field  #stored in cloud(media)
    
    def __str__(self):
        return f'{self.lesson_number} {self.lesson_name}'
    class Meta:
        db_table = 'lessons'
        ordering = ["lesson_number"]
        
        
class Question(CommonFields): 
    """
    Represents a question related to a module.
    Attributes:
        module: The module to which this question belongs.
        question: The text of the question.
        answer_type: The type of answer expected, filtered by choice type "answer"(multiple, single)
    Methods:
        __str__(): Returns the question text.
    Meta:
        db_table: Specifies the database table name as 'questions'.
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name= 'module_question')
    question = models.CharField(max_length=255)
    answer_type = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'choice_type': 'answer'}, related_name='question_type')
    
    def __str__(self):
        return self.question
    class Meta:
        db_table = 'questions'
        
        
class Answers(CommonFields):
    """
    Represents answer options for a question.
    Attributes:
        question: The question to which this answer belongs.
        options: The text of the answer option.
        is_correct: Indicates whether the answer is correct.
    Methods:
        __str__(): Returns the text of the answer option.
    Meta:
        db_table: Specifies the database table name as 'answers'.
        unique_together: Ensures that each question has unique answer options.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='question_options_question',
    )
    options = models.CharField(max_length=255,) 
    is_correct = models.BooleanField(null=True, blank=True, default=False)
    

    def __str__(self):
        return f'{self.options}'

    class Meta:
        db_table = 'answers'
        unique_together = ('question', 'options')
        
        
    
class Assignee(CommonFields):
    """
    Represents an assignment of a course to a user.
    Attributes:
        course: The course assigned to the user.
        user: The user to whom the course is assigned.
    Methods:
        __str__(): Returns a string representation of the assignee, including the user's name and designation.
    Meta:
        db_table : Specifies the database table name as 'assignees'.
        unique_together: Ensures that a user cannot be assigned the same course multiple times.
    """

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='assignee_course', blank=True,null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assignee_user')
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        db_table = 'assignees'
        unique_together = ('course', 'user') 
    
    
    
class UserScore(CommonFields):
    """
    Model to store users' scores for lessons.
    Attributes:
        user: References the CustomUser model, linking the score to a specific user.
        lesson : References the Lesson model, allowing scores to be associated with a specific lesson.
        attempts: Stores the number of attempts made by the user.
        score_achieved : Stores the score obtained by the user (up to 4 digits, with 2 decimal places).
        test_result : References the Choice model, storing the test result with a restriction on 'choice_type' being 'test_result'.(complete/inprogress)
    Meta:
        db_table : Defines the database table name as 'user_scores'.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_score')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='lesson_score', blank=True, null=True)
    attempts = models.PositiveIntegerField()
    score_achieved = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True,)
    test_result = models.ForeignKey(Choice, on_delete=models.SET_NULL, related_name='test_result', limit_choices_to={'choice_type': 'test_result'}, blank=True, null=True )
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Lesson: {self.lesson.lesson_name}, Score: {self.score_achieved}"

    class Meta:
        db_table = 'user_scores'


class UserAnswer(CommonFields):
    """
    Model to store users' answers for questions.
    Attributes:
        user: Links the answer to a specific user.
        answer: References the Answers model, storing the selected answer.
        user_answer: Stores the user's text-based answer.
    Methods:
        __str__(): Returns a string representation displaying the user's name 
    Meta:
        db_table: Defines the database table name as 'user_answers'.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='users')
    que = models.ForeignKey(Question, on_delete=models.SET_NULL, related_name='user_question', blank=True, null=True)
    user_answer = models.TextField(blank=True, null=True)    
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        db_table = 'user_answers'
        
        
    
    
   
