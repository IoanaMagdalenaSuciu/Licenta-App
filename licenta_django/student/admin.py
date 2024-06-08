from django.contrib import admin

# Register your models here.
from student.models import Student, Interest, Goal, Question, Choice

admin.site.register(Student)
admin.site.register(Interest)
admin.site.register(Goal)
admin.site.register(Question)
admin.site.register(Choice)
