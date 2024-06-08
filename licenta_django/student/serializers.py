from rest_framework import serializers
from .models import Student, Question, Choice, Goal, Interest


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ('pk', 'user', 'first_name', 'last_name', 'email', 'date_of_birth', 'interests', "goals", "level", "vark_model")

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('pk', 'choice')

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(read_only=True, many=True)
    class Meta:
        model = Question
        fields = ('pk', 'question', 'choices')

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ('pk', 'name')

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('pk', 'name')