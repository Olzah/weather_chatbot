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
        "description": "Get the current weather",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "format": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use. Infer this from the users location.",
                },
            },
            "required": ["location", "format"],
        },
    },
    {
        "name": "get_n_day_weather_forecast",
        "description": "Get an N-day weather forecast",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "format": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The temperature unit to use. Infer this from the users location.",
                },
                "name_day": {
                    "type": "string",
                    "enum": ["aftertomorrow", "tomorrow"],
                    "description": "The name of the days to forecast, used if user ask about tomorrow or after tomorrow",
                }
            },
            "required": ["location", "format", "num_days"]
        },
    },
]


def chat_completion_request(messages, functions=None, function_call=None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }

    json_data ={"model": model, "messages": messages}
    
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