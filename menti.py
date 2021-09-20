import json
import requests as rq

identifier_URL = "https://www.menti.com/core/identifiers"
identifiers = []

identifier_series_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " 
    + "(KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
}

def find_question(questions: dict, public_key: str):
    for question in questions:
        if question["public_key"] == public_key:
            return question

def get_identifier():
    identifier_request = rq.post(identifier_URL, headers=identifier_series_headers)

    if identifier_request.status_code == 200:
        identifier_response = json.loads(identifier_request.text)
        identifier = identifier_response["identifier"]
        identifiers.append(identifier)
        return identifier
    else:
        print("\nRequest URL:", identifier_URL)
        print("Status code:", identifier_request.status_code)
        print("Response body:", identifier_request.text)
        raise(Exception("We couldn't retrieve an identifier for this menti!"))

def get_menti_info(menti_ID: str):
    series_URL = f"https://www.menti.com/core/vote-keys/{menti_ID}/series"
    series_request = rq.get(series_URL, headers=identifier_series_headers)
    
    if series_request.status_code == 200:
        series_response = json.loads(series_request.text)
        return series_response
    else:
        print("\nRequest URL:", series_URL)
        print("Status code:", series_request.status_code)
        print("Response body:", series_request.text)
        raise(Exception("We couldn't fetch any information on this menti!"))