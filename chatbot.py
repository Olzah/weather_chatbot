import openai
from dotenv import load_dotenv
from datetime import timedelta, datetime
import chainlit as cl
from src.llm import chat_completion_request, messages, functions
from src.utils import get_current_weather
import json
import os


day = ""
load_dotenv()

def execute_function_call(assistant_messages):
    if assistant_messages.get("function_call").get("name") == "get_current_weather":
        location = json.loads(assistant_messages.get("function_call").get("arguments"))["location"]
        day_loc = json.loads(assistant_messages.get("function_call").get("arguments"))["weather_day"]
        global day
        if day_loc == "today":
            day = datetime.now().strftime('%Y-%m-%d')
        elif day_loc == "tomorrow":
            day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        elif day_loc == "aftertomorrow":
            day = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
          
        result = get_current_weather(location)
    
    else:
        result = f"Error message, assistance msg dosent have exist function"
    return result

def get_natural_response(content):
    convert_prompt = f"Convert result from Open weather map api to a natural sentense: {content}"
    messages.append({"role": "user", "content": convert_prompt})
    convert_promp_response = chat_completion_request(messages=messages)
    new_assistant_message = convert_promp_response.json()["choices"][0]["message"]
    messages.append(new_assistant_message)
    content = new_assistant_message["content"]
    return content

@cl.on_message
async def main(message: str):
    messages.append({"role": "user", "content": message})
    chat_response = chat_completion_request(messages=messages, functions=functions)
    assistance_message = chat_response.json()["choices"][0]["message"]
    
    if assistance_message.get("function_call"):
        result = execute_function_call(assistance_message)
        content = []
        for forecast in result['list']:
            forecast_date = forecast['dt_txt'].split()[0]
            if forecast_date == day:
                content.append(json.dumps(forecast))
        content = get_natural_response(content)
        
    else:
        messages.append(assistance_message)
        content = assistance_message["content"]

    await cl.Message(
        content = content
    ).send()
 
