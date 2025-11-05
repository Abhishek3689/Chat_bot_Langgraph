from langchain_core.tools import tool
from langchain_tavily import TavilySearch
import os
import requests
from dotenv import load_dotenv

load_dotenv()

weather_key=os.getenv("WEATHER_API_KEY")

@tool
def Weather_data(city:str):
    """
    This Fucntion Fetches weather data of a particular region
    """
    url="https://api.weatherapi.com/v1/current.json?"
    params={
        "key":weather_key,
        "q":city,
        "aqi":"no"
    }
    response=requests.get(url,params=params)
    data=response.json()
    return data

web_search=TavilySearch(max_results=5,
                        topic="general")
@tool
def calculator(first_num:int,second_num:int,operation:str):
    """
    Perform a basic arithmetic operation on two numbers.
    Supported operations: add, sub, mul, div
    """
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "sub":
            result = first_num - second_num
        elif operation == "mul":
            result = first_num * second_num
        elif operation == "div":
            if second_num == 0:
                return {"error": "Division by zero is not allowed"}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation '{operation}'"}
        
        return {"first_num": first_num, "second_num": second_num, "operation": operation, "result": result}
    except Exception as e:
        return {"error": str(e)}
    
