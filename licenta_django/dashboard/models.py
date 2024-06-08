from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from student.models import Student


class Course(models.Model):
    name = models.CharField(max_length=200)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(_('enrollment date'))
    grade = models.DecimalField(_('grade'), max_digits=5, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        unique_together = ('student', 'course')

class CourseProject(models.Model):
    enrollement = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='courseprojects')
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=1000)
    requirements = models.JSONField()

class Test(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="tests")
    questions = models.JSONField()
