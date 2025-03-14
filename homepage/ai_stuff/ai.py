import sys
import requests
import pprint
from time import sleep
from datetime import datetime
from random import choice

# store globals
auth_key = "47b32e758a344b379770d421e20c95b6"
headers = {"authorization": auth_key, "content-type": "application/json"}

transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
upload_endpoint = "https://api.assemblyai.com/v2/upload"

# This is for demo purposes because it take less time
def demo_sentiment_provider(file_path):
    return "positive"


# this took a longer time because assemblyAI offered a longer response time api for students so we
# decided to implement it for proof of concept but we didnt use this in the demo because it might take
# too much of our pitch time
def sentiment_eval(response_json):
    value_sentiment = 0
    for phrase in response_json["sentiment_analysis_results"]:
        curr_sentiment = phrase["sentiment"]
        if curr_sentiment == "POSITIVE":
            value_sentiment += 1
        elif curr_sentiment == "POSITIVE":
            value_sentiment -= 1

    if value_sentiment > 0:
        return "positive"
    elif value_sentiment < 0:
        return "negative"
    else:
        return "neutral"


def sentiment_eval(response_json):
    value_sentiment = 0
    for phrase in response_json["sentiment_analysis_results"]:
        curr_sentiment = phrase["sentiment"]
        if curr_sentiment == "POSITIVE":
            value_sentiment += 1
        elif curr_sentiment == "POSITIVE":
            value_sentiment -= 1

    if value_sentiment > 0:
        return "positive"
    elif value_sentiment < 0:
        return "negative"
    else:
        return "neutral"


# Unused due to high time for taken by the assemblyAI API to return results
# OPTIONAL
def sentiment_provider_with_ai(file_path):
    # reads audio file
    def read_file(filename):
        with open(filename, "rb") as _file:
            while True:
                data = _file.read(5242880)
                if not data:
                    break
                yield data

    # upload our audio file
    upload_response = requests.post(
        upload_endpoint, headers=headers, data=read_file(file_path)
    )
    print("Audio file uploaded")

    # send a request to transcribe the audio file
    transcript_request = {
        "audio_url": upload_response.json()["upload_url"],
        "sentiment_analysis": "true",
    }
    transcript_response = requests.post(
        transcript_endpoint, json=transcript_request, headers=headers
    )
    print("Transcription Requested")
    pprint.pprint(transcript_request)
    pprint.pprint(transcript_response.json())
    prev_time = datetime.now()
    # set up polling
    polling_response = requests.get(
        transcript_endpoint + "/" + transcript_response.json()["id"], headers=headers
    )
    # filename = transcript_response.json()["id"] + ".txt"

    # if our status isn’t complete, sleep and then poll again
    while polling_response.json()["status"] != "completed":
        sleep(1)
        polling_response = requests.get(
            transcript_endpoint + "/" + transcript_response.json()["id"],
            headers=headers,
        )
        print("File is", polling_response.json()["status"])
    # pprint(polling_response)

    s = sentiment_eval(polling_response.json())
    new_time = datetime.now()
    elapsed = new_time - prev_time
    print(elapsed.seconds, ":", round(elapsed.microseconds, 2))
    print(s)
    return s
