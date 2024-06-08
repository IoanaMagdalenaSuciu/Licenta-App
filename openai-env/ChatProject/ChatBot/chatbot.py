import os
import json
import requests
from django.http import HttpResponse
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler

client = OpenAI()
model = "gpt-3.5-turbo-0125"
ASSISTANT_ID = "asst_CRMgJMP2W11Nfygd1HTukz0Y"
thread = client.beta.threads.create()


class Text:
    def __init__(self, value):
        self.value = value

class TextContentBlock:
    def __init__(self, text):
        self.text = text

class Message:
    def __init__(self, content):
        self.content = content

class SyncCursorPage:
    def __init__(self, data):
        self.data = data


class StudentDetails:
    _instance = None
    _student_data = None

    def __new__(cls, student_id):
        if cls._instance is None:
            cls._instance = super(StudentDetails, cls).__new__(cls)
            cls._fetch_student_details(student_id)
        return cls._instance

    @classmethod
    def _fetch_student_details(cls, student_id):
        url = f'http://localhost:8000/api/student_details/{student_id}'
        response = requests.get(url)
        if response.status_code == 200:
            cls._student_data = response.json()
        else:
            cls._student_data = None

    @classmethod
    def get_student_data(cls):
        return cls._student_data
    
    def __getitem__(self, key):
        if self._student_data:
            return self._student_data.get(key)
        return None


def generate_response(question, student_id, api_key=None, max_tokens=100):
    response = ""
    student_details = StudentDetails(student_id)
    print(student_details)
    instructions = create_system_request(student_details)

    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role="user",
        content= question
        )
    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=ASSISTANT_ID,
    instructions= instructions
    )

    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id,
            limit=1
        )
        text = extract_text_from_response(messages)
        
        response += text
    else:
        print(run.status)
    return response

def extract_text_from_response(response):
    try:
        first_message = response.data[0]
        
        first_content_block = first_message.content[0]
        
        extracted_text = first_content_block.text.value
        
        return extracted_text
    except (AttributeError, IndexError) as e:
        # Handle the case where the expected attributes are not found
        print(f"Error extracting text: {e}")
        return None

def create_system_request(data):
    print(data["goals"])
    base_request = (
        "Assist This student. The student's profile data, including interests, goals, level of knowledge in computer science, enrolled courses, and learning style, is provided in JSON format. "
        "The student details in a JSON format: "
        + str({
            'first_name': data['student'],
            'interests': data['interests'],
            'goals': data['goals'],
            'level_of_knowledge': data['level'],
            'learning_data': data['learning_data'],
            'vark_model': data['vark_model'], 
            'assigned_projects': data['projects'],
        })
        )
    return base_request


def generate_project(course_name, course_description, level, vark_model):
    instructions = ("Create a project for a student whith a level of understanding the domain og" + level + " and is a " + vark_model + " learner. The response will be generated in a JSON form as follows: name, description, requirements.")
    print("Instuctions done")
    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role="user",
        content= f"Clease create a project for a course named {course_name} the course description is {course_description}. The project will be designe for a specific student taking into consideration that the student has o level of understanging of the domaine {level} and is a {vark_model} learner. The requirements of this project will consist in a stept by step list of what the student should do (maximum 5 stepts) and the description will consist in a high level description of the project. The response will be generated in a JSON form as follows: name, description, requirements."
        )
    print("message sent")
    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=ASSISTANT_ID,
    instructions= instructions
    )
    print("thread run")
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id,
            limit=1
        )
        text = extract_text_from_response(messages)
        print(text)
        response = text
    else:
        print(run.status)
    print(response)
    return response
