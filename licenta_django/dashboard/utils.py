from dashboard.models import Course, Enrollment, CourseProject
from dashboard.serializers import EnrollmentSerializer
from student.models import Student
from datetime import date, timedelta
import requests

def save_courses(ontology_courses, pk):
    student = Student.objects.get(pk=pk)
    courses = []
    enrollments = []
    print(ontology_courses)
    for course_name in ontology_courses:
        course, created = Course.objects.get_or_create(name=course_name)
        print("Created course:", course)
        courses.append(course)
        enrollment_data = {
            'student': student.id,
            'course': course.id,
            'enrollment_date': date.today(),
        }
        enrollment, enrollment_created = Enrollment.objects.get_or_create(student=student, course=course,
                                                                          defaults={'enrollment_date': date.today(),
                                                                                    'status': 'enrolled'})
        enrollments.append(enrollment)
    serialized_enrollments = EnrollmentSerializer(enrollments, many=True).data
    return serialized_enrollments

def create_project(course, student, enrollment):
    url = f'http://localhost:9000/api/project/'
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    }
    data = {
        "courseName": course['name'],
        "courseDescription": course['description'],
        'level': course['level'],
        'vark_model': student.vark_model.replace('"', '')
    }
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        print('Request was successful')
        parsed_data =  response.json()
        project, created = CourseProject.objects.get_or_create(enrollement= enrollment, name= parsed_data['name'], description= parsed_data['description'], requirements= parsed_data['requirements'])
        return project
        print('Response data:', response.json())
    else:
        print('Request failed')
        print('Status code:', response.status_code)
        print('Response:', response.text)
    


