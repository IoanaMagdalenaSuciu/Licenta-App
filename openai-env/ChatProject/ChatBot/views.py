from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ChatBot.chatbot import generate_project
import json
# Create your views here.

@api_view(['POST'])
def get_project(request):
  courseName = request.data.get("courseName")
  courseDescription = request.data.get("courseDescription")
  level = request.data.get("level")
  vark_model = request.data.get("vark_model")
  response = generate_project(courseName, courseDescription, level, vark_model)
  decoder = json.JSONDecoder()
  data = decoder.decode(response)
  print(data)
  return Response(data, status=status.HTTP_201_CREATED)  