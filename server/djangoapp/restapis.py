# Uncomment the imports below before you add the function code
import json
import requests
import os
from pathlib import Path
from urllib.parse import quote
from dotenv import dotenv_values

_env_path = Path(__file__).resolve().parent / ".env"
_env = dotenv_values(_env_path)

# Prefer djangoapp/.env over lab-injected env (Skills Network often sets backend_url to :8000)
backend_url = (
    _env.get("backend_url")
    or os.getenv("backend_url")
    or "http://localhost:3030"
).rstrip("/")
_sentiment_url = (
    _env.get("sentiment_analyzer_url")
    or os.getenv("sentiment_analyzer_url")
    or "http://localhost:5050/"
)
# Ignore lab placeholder until Code Engine URL is set in djangoapp/.env
if _sentiment_url and "code engine" in _sentiment_url.lower():
    _sentiment_url = "http://localhost:5050/"
sentiment_analyzer_url = _sentiment_url.rstrip("/") + "/"
print(f"Using backend_url={backend_url} (from {_env_path})")
print(f"Using sentiment_analyzer_url={sentiment_analyzer_url}")

# def get_request(endpoint, **kwargs):
def get_request(endpoint, **kwargs):
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        # If any error occurs
        print(f"Network exception occurred: {err}")
        return []


# Add code for get requests to back end
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + quote(text, safe="")
    try:
        response = requests.get(request_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, str):
            data = json.loads(data)
        return data if isinstance(data, dict) else {"sentiment": "neutral"}
    except Exception as err:
        print(f"Sentiment analyzer error: {err}")
        return {"sentiment": "neutral"}

# def analyze_review_sentiments(text):
# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments
def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")

# def post_review(data_dict):
# Add code for posting review
