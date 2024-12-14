import allure
import pytest
from faker import Faker

from src.assertions import Assertions
from src.base_case import BaseCase
from src.my_requests import MyRequests


@allure.epic("Register user cases")
class TestUserRegister(BaseCase):
    @allure.feature("Positive cases")
    @allure.title("Create user successfully")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.feature("Negative cases")
    @allure.title("Create user with existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content '{response.content}'"

    @allure.feature("Negative cases")
    @allure.title("Create user with incorrect email format")
    def test_create_user_with_incorrect_email(self):
        email = 'incorrect_email.com'
        data = self.prepare_registration_data(email)
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Invalid email format", f"Unexpected response content '{response.content}'"

    @allure.feature("Negative cases")
    @allure.title("Create user without mandatory parameter")
    @pytest.mark.parametrize("delete_key", [
        "username",
        "firstName",
        "lastName",
        "email",
        "password"
    ])
    def test_create_user_without_mandatory_param(self, delete_key):
        data = self.prepare_registration_data()
        del data[delete_key]
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {delete_key}", f"Unexpected response content '{response.content}'"

    @allure.feature("Negative cases")
    @allure.title("Create user with short 'username' value")
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        data["username"] = "A"
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too short", f"Unexpected response content '{response.content}'"

    @allure.feature("Negative cases")
    @allure.title("Create user with long 'username' value")
    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        fake = Faker()
        data["username"] = fake.pystr(min_chars=251, max_chars=260)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too long", f"Unexpected response content '{response.content}'"
