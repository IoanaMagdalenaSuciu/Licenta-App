from rest_framework import serializers

from dashboard.models import Enrollment, Course, CourseProject, Test


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'enrollment_date', 'grade', 'status']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course('name')

class CourseProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseProject
        fields = ('enrollement', 'name', 'description', 'requirements')

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('enrollement', 'questions')