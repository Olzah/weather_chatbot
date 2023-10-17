import openai
from dotenv import load_dotenv
from datetime import timedelta, datetime
import chainlit as cl
from src.llm import chat_completion_request, messages, functions
from src.utils import get_current_weather, get_n_day_weather_forecast
import json
import os


day = ""
load_dotenv()

def execute_function_call(assistant_messages):
    location = json.loads(assistant_messages.get("function_call").get("arguments"))["location"]
    format = json.loads(assistant_messages.get("function_call").get("arguments"))["format"]
    
    if assistant_messages.get("function_call").get("name") == "get_current_weather":
        result = get_current_weather(location, format)
    elif assistant_messages.get("function_call").get("name") == "get_n_day_weather_forecast":
        name_day = json.loads(assistant_messages.get("function_call").get("arguments"))["name_day"]
        global day
        if name_day == "tomorrow":
            day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        elif name_day == "aftertomorrow":
            day = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        return get_n_day_weather_forecast(location, format, day)
    else:
        result = f"Error message, assistance msg dosent have exist function"
        return result

def get_natural_response(content):
    convert_prompt = f"Return the average value for the day, such as the maximum temperature, etc: {content}"
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
    print(f"SIMPLE JSON: {chat_response.json()}")
    assistance_message = chat_response.json()["choices"][0]["message"]
    
    if assistance_message.get("function_call") and assistance_message.get("function_call")['name'] == "get_n_day_weather_forecast":
        content = execute_function_call(assistance_message)
        content = get_natural_response(content)
    elif assistance_message.get("function_call") and assistance_message.get("function_call")["name"] == "get_current_weather":
        content = execute_function_call(assistance_message)
        content = get_natural_response(content)
    else:
        messages.append(assistance_message)
        content = assistance_message["content"]

    await cl.Message(
        content = content
    ).send()
 
