from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User

from dashboard.models import Course, Enrollment, CourseProject
from student.models import Student, Question, Goal, Interest
from student.serializers import StudentSerializer, QuestionSerializer, GoalSerializer, InterestSerializer
from student.utils import calculate_vark_model, calculate_level_model
from datetime import datetime
from ontology.utils import compute_learning_data, compute_course_details, add_student

@api_view(['GET'])
def students(request):
    if request.method == 'Get':
        data = Student.objects.all()
        serializer = StudentSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create_student(request):
    user_data = request.data.get('user')
    selected_goals = request.data.get('goals')
    selected_interests = request.data.get('interests')

    # Create user with goals and interests
    user = User.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'],
    )

    # Create or retrieve interests and goals
    interests = []
    for interest_name in selected_interests:
        interest, created = Interest.objects.get_or_create(name=interest_name)
        interests.append(interest)

    goals = []
    for goal_name in selected_goals:
        goal, created = Goal.objects.get_or_create(name=goal_name)
        goals.append(goal)

    # Create Student object
    student_data_for_ontology = {
        'username': user_data['username'],
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        'email': user_data['email'],
        'date_of_birth': datetime.strptime(user_data['date_of_birth'], '%Y-%m-%d').date(),
        'interests': [interest.name for interest in interests],  # Make sure to pass IDs
        'goals': [goal.name for goal in goals],
        'level': user_data['level'], 
        'vark_model': user_data['vark_model'].replace('"', ""),
    }
    student_serializer = StudentSerializer(data={
        'user': user.id,
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        'email': user_data['email'],
        'date_of_birth': datetime.strptime(user_data['date_of_birth'], '%Y-%m-%d').date(),
        'interests': [interest.id for interest in interests],  # Make sure to pass IDs
        'goals': [goal.id for goal in goals],
        'level': user_data['level'], 
        'vark_model': user_data['vark_model'],
    })

    if student_serializer.is_valid():
        student_serializer.save()

        # Associate interests and goals with the student
        student = student_serializer.instance
        student.interests.add(*interests)
        student.goals.add(*goals)
        add_student(student_data=student_data_for_ontology)
        return Response(student_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_by_username_and_password(request):
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')
    try:
        users = User.objects.all()
        user = User.objects.get(username=username)
        if user.check_password(password):
            student = Student.objects.get(user=user)
            serializer = StudentSerializer(student, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
def vark_questions(request):
    data = Question.objects.filter(is_vark=True)
    serializer = QuestionSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def level_questions(request):
    data = Question.objects.filter(is_vark=False)
    serializer = QuestionSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def vark_model(request):
    vark_model = calculate_vark_model(request.data)
    print("Dominant Learning Style: ", vark_model)
    return Response(vark_model, status=status.HTTP_200_OK)

@api_view(["POST"])
def level_model(request):
    level_model = calculate_level_model(request.data)
    print("Level: ", level_model)
    return Response(level_model, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_goals_by_id(request, goal_id):
    data = Goal.objects.filter(pk=goal_id)
    serializer = GoalSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_interests_by_id(request, interest_id):
    data = Interest.objects.filter(pk=interest_id)
    serializer = InterestSerializer(data, context={'request': request}, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_student_courses(request, student_id):
    student = Student.objects.get(pk=student_id)
    enrollments = Enrollment.objects.filter(student=student)
    course_names = [enrollment.course.name for enrollment in enrollments]
    learning_data = compute_learning_data(course_names)
    return Response(learning_data, status=status.HTTP_200_OK)



@api_view(["GET"])
def student_details(request, student_id):
    student = Student.objects.get(pk=student_id)
    response = {}
    response['student'] = student.first_name
    response['vark_model'] = student.vark_model
    response['level'] = student.level
    response['interests'] = [interest.name for interest in student.interests.all()]
    response['goals'] = [goal.name for goal in student.goals.all()]

    enrollments = Enrollment.objects.filter(student=student)
    course_names = [enrollment.course.name for enrollment in enrollments]
    projects =  CourseProject.objects.filter(enrollement__in=enrollments)
    learning_data = compute_learning_data(course_names)
    response['learning_data'] = learning_data
    response['projects'] = []
    for project in projects:
        project_info = {
            "project_name": project.name,
            "project_description": project.description,
            "project_requirements": project.requirements,
        }
        response['projects'].append(project_info)

    return Response(response, status=status.HTTP_200_OK)