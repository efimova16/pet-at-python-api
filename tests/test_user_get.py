import allure

from src.assertions import Assertions
from src.base_case import BaseCase
from src.my_requests import MyRequests


@allure.epic("Get user cases")
class TestUserGet(BaseCase):
    @allure.feature("Negative cases")
    @allure.title("Get user data without authorization")
    def test_get_user_details_not_auth(self):
        response = MyRequests.get(f"/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")
        Assertions.assert_json_has_not_key(response, "email")

    @allure.feature("Positive cases")
    @allure.title("Get user data successfully")
    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(
            f"/user/{self.user_id_from_auth_method}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )

        Assertions.assert_json_has_keys(response2, ["username", "firstName", "lastName", "email"])
