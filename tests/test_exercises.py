import json

import pytest
import requests

from src.assertions import Assertions
from src.base_case import BaseCase


class TestExercises(BaseCase):
    params = [
        (
        "Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
        '{"platform": "Mobile", "browser": "No", "device": "Android"}'),
        (
        "Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
        '{"platform": "Mobile", "browser": "Chrome", "device": "iOS"}'),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
         '{"platform": "Googlebot", "browser": "Unknown", "device": "Unknown"}'),
        (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
        '{"platform": "Web", "browser": "Chrome", "device": "No"}'),
        (
        "Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        '{"platform": "Mobile", "browser": "No", "device": "iPhone"}')
    ]

    def test_ex10(self):
        phrase = input("Set a phrase: ")
        assert len(
            phrase) < 15, f"Тhe phrase is not shorter than 15 characters, the length of the phrase is {len(phrase)}"

    def test_ex11(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print(response.cookies)
        cookie_value = self.get_cookie(response, "HomeWork")
        assert cookie_value == "hw_value", "Wrong value for 'HomeWork' cookie"

    def test_ex12(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(response.headers)
        header_value = self.get_header(response, "x-secret-homework-header")
        assert header_value == "Some secret value", "Wrong value for 'x-secret-homework-header'"

    @pytest.mark.parametrize('user_agent, exp_result', params)
    def test_ex13(self, user_agent, exp_result):
        response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check",
                                headers={"User-Agent": user_agent})

        exp_result_as_dict = json.loads(exp_result)

        Assertions.assert_json_value_by_name(
            response,
            "platform",
            exp_result_as_dict["platform"],
            f"Wrong platform value for '{user_agent}'"
        )

        Assertions.assert_json_value_by_name(
            response,
            "device",
            exp_result_as_dict["device"],
            f"Wrong device value for '{user_agent}'"
        )

        Assertions.assert_json_value_by_name(
            response,
            "browser",
            exp_result_as_dict["browser"],
            f"Wrong browser value for '{user_agent}'"
        )
