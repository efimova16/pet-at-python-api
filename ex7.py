import requests

param = {}

print("######### 1 #########")
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(response.text)

print("######### 2 #########")
param.update({"method": "HEAD"})
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=param)
print(response.text)

print("######### 3 #########")
param.update({"method": "GET"})
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=param)
print(response.text)

print("######### 4 #########")
methods = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH", "TRACE", "CONNECT"]
for x in methods:
    param.update({"method": x})
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=param)
    print(f"GET request with param {x}:" + response.text)
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
    print(f"POST request with param {x}:" + response.text)
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
    print(f"PUT request with param {x}:" + response.text)
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=param)
    print(f"DELETE request with param {x}:" + response.text)
