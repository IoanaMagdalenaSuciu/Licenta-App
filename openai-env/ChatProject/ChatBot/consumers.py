import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ChatBot.chatbot import generate_response

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        question = text_data_json['message']
        student_id = text_data_json['student']

        # Generate response using ChatGPT
        response = generate_response(question, student_id, api_key="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")
        print (response)
        await self.send(text_data=json.dumps({
            'message': response
        }))