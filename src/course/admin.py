from django.contrib import admin
from course.models import Category, Course, Module, Lesson, Question, Assignee, UserScore, Answers

# Register your models here.
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(Answers)
admin.site.register(Assignee)
admin.site.register(UserScore)
# admin.site.register(UserAnswer)





