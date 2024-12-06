import time
from json.decoder import JSONDecodeError

import requests

param = {}
url = "https://playground.learnqa.ru/ajax/api/longtime_job"

try:
    response = requests.get(url)
    print(response.text)
    parsed_response_text = response.json()
    token = parsed_response_text["token"]
    seconds = parsed_response_text["seconds"]

    if token is not None:
        param.update({"token": token})
        parsed_resp_text = requests.get(url, param).json()
        assert parsed_resp_text["status"] == "Job is NOT ready"

        time.sleep(seconds)

        parsed_resp_text = requests.get(url, param).json()
        assert parsed_resp_text["status"] == "Job is ready"
        assert parsed_resp_text["result"] is not None
except JSONDecodeError:
    print("Response is not a JSON")
