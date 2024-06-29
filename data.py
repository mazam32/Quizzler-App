import requests

question_data = []

response = requests.get("https://opentdb.com/api.php?amount=10&type=boolean")
response.raise_for_status()
for each_thing in response.json()["results"]:
    question_data.append(each_thing)
