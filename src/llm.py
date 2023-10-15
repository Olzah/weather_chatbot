import os
import openai
import requests
import datetime
import json
from datetime import datetime, timedelta
from src.sys_config import system_instruction
next_day = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
from dotenv import load_dotenv

load_dotenv()
GPT_MODEL = "gpt-3.5-turbo-0613"
WEATH_KEY = ""
OPENAI_KEY = api_key = os.environ.get("OPENAI_KEY")

openai.api_key = OPENAI_KEY

messages = [
    {"role": "system", "content": system_instruction}
]

functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location and date",
        "parameters": {
            "type": "object",
            "properties": { 
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "weather_day": {
                     "type": "string",
                     "description": "The day like tomorrow, today, aftertomorow. Current its means also today",
                }
            },
            "required": [
                "location",
                "weather_day"
                ],
        },
    },
]

def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }

    json_data ={
        "model": model,
        "messages": messages
    }
    if functions is not None:
        json_data.update({"functions": functions})
    if function_call is not None:
        json_data.update({"function_call": function_call})
    try:
        response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=json_data,
        )
        return response       
    except Exception as e:
        print(f"\n Unable to generate ChatCompletion response")
        print(f"\n Exception: {e}")
        raise e