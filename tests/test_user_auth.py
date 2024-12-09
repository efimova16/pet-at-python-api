import pytest
import requests

from src.assertions import Assertions
from src.base_case import BaseCase


class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    # https: // docs.pytest.org / en / stable / how - to / xunit_setup.html
    def setup_method(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        # self служит указателем, который позволяет расширить область видимости переменных:
        # при объявлении переменной внутри метода класса она доступна только в рамках этого метода.
        # Однако, если объявить её с использованием указателя self, то она станет доступной для всех методов этого класса
        # и его наследников. При этом доступ к этой переменной всегда должен осуществляться через self.
        # то есть self делает переменную полем класса и позволяет шарить ее между  методами\тестами класса
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    def test_auth_user(self):
        response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                 headers={"x-csrf-token": self.token}, cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth_method,
            "user_id_from_check_method is not equal user_id_from_auth_method"
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_user(self, condition):
        if condition == "no_cookie":
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     headers={"x-csrf-token": self.token})
        else:
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     cookies={"auth_sid": self.auth_sid})
        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
