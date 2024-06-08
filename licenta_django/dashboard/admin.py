from django.contrib import admin

# Register your models here.
from dashboard.models import Course, Enrollment, CourseProject, Test

admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(CourseProject)
admin.site.register(Test)