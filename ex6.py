import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

for x in response.history:
    print(x.text)
    print(x.status_code)

print(len(response.history))
print(response.url)
