
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import query_class_instances, query_class_instances_by_part, calculate_curricula
from student.utils import prepare_data_for_curricula
from dashboard.utils import save_courses
from django.contrib.auth.models import User

@api_view(['GET'])
def get_goals(request):
    # Load the ontology file into a Graph object
    # g = load_ontology(True)

    # Query the ontology for instances of the 'YourClass' class
    instances = query_class_instances('Goal')

    # Render the template with the list of instances
    return Response(instances)

@api_view(['GET'])
def get_interests(request):
    # g = load_ontology(True)
    instances = query_class_instances( "Interest")
    return Response(instances)

@api_view(['GET'])
def all_domains(request):
    # g = load_ontology(True)
    instances = query_class_instances("Domain")
    return Response(instances)

@api_view(['GET'])
def courses_by_domain(request, domain_name):
    # g = load_ontology(True)
    instances = query_class_instances_by_part("Course", domain_name)
    return Response(instances)

@api_view(["POST"])
def generate_curricula(request):
    user = User.objects.filter(pk=request.data["user_id"])[0]
    result = calculate_curricula(user.username)
    print(result)
    response = save_courses(result, request.data['pk'])
    return Response(response)