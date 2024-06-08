from django.shortcuts import render
import json
from .models import Student, Course, Enrollment
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from student.models import Student
from dashboard.models import Course, CourseProject, Test
from ontology.utils import compute_course_details, retrieve_course_from_ontology, get_computer_science_domains
from dashboard.serializers import CourseProjectSerializer
from dashboard.utils import create_project
from student.utils import get_student_models
def home(request):
    student = Student.objects.get(user=request.user)

    courses_in_progress = Enrollment.objects.filter(student=student).values('course')

    courses = Course.objects.filter(id__in=courses_in_progress)

    return render(request, 'dashboard/home.html', {'courses': courses, 'student': student})

@api_view(["GET"])
def course_details(request, student_id, course_name):
    student = Student.objects.get(pk=student_id)
    course = Course.objects.filter(name=course_name.replace("_", " ")).first()
    enrollement = Enrollment.objects.filter(student=student, course=course).first()
    print("course", course)
    print("student", student)
    print("enrollement", enrollement)
    course_details = compute_course_details(course_name)
    course_details['status'] = enrollement.status
    course_details['enrollement'] = enrollement.pk
    print(course_details)
    return Response(course_details, status=status.HTTP_200_OK)

@api_view(["POST"])
def update_course_status(request):
    enrollment = Enrollment.objects.get(pk= request.data["enrollement"])
    enrollment.status = request.data["status"]
    enrollment.save()
    print(enrollment)
    return Response("succes", status=status.HTTP_200_OK)

@api_view(["GET"])
def get_project_by_enrollment(request, enrollement_id):
    enrollement = Enrollment.objects.get(pk=enrollement_id)
    data = CourseProject.objects.filter(enrollement=enrollement).first()
    onto_course = retrieve_course_from_ontology(enrollement.course.name)
    if not data:
        data = create_project(onto_course, enrollement.student, enrollement)
        serializer = CourseProjectSerializer(data, context={'request': request}, many=False)
        print("DATA", data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = CourseProjectSerializer(data, context={'request': request}, many=False)
    print("DATA", data)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_current_courses(request, student_id):
    student = Student.objects.get(pk=student_id)
    enrollements = Enrollment.objects.filter(student = student)
    response = {"courses": enrollements.count()}
    return Response(response, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_student_data(request, student_id):
    student = Student.objects.get(pk=student_id)
    enrollements = Enrollment.objects.filter(student=student)
    projects =  CourseProject.objects.filter(enrollement__in=enrollements)
    tests = Test.objects.filter(enrollment__in=enrollements)
    response = {
        "courses": enrollements.count(),
        "projects": projects.count(),
        "tests": tests.count(),
    }
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_stats(request):
    vark = get_student_models()
    courses = [course.name for course in Course.objects.all()]
    computer_science_domains = get_computer_science_domains(courses)
    response ={
        "vark":vark,
        "computer_science_domains": computer_science_domains
    }
    return Response(response, status=status.HTTP_200_OK)