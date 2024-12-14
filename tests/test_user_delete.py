import allure

from src.assertions import Assertions
from src.base_case import BaseCase
from src.my_requests import MyRequests


@allure.epic("Delete user cases")
class TestUserDelete(BaseCase):
    @allure.feature("Positive cases")
    @allure.title("Delete user successfully")
    def test_delete_user_successfully(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        last_name = register_data["lastName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_code_status(response3, 200)
        Assertions.assert_json_value_by_name(response3, "success", "!", f"Wrong response '{response3.content}'")

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_code_status(response4, 404)
        assert response4.text == "User not found", f"Wrong response text. Actual response is: '{response4.text}'"

    @allure.feature("Negative cases")
    @allure.title("Delete user with id=2")
    def test_delete_user_with_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.delete(
            f"/user/2",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(response2, "error",
                                             "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",
                                             f"Wrong response '{response2.content}'")

    @allure.feature("Negative cases")
    @allure.title("Delete user with other user auth data")
    def test_delete_user_with_other_user_auth_data(self):
        register_data_1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data_1)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id_1 = self.get_json_value(response1, "id")

        register_data_2 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data_2)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        login_data = {
            'email': register_data_2["email"],
            'password': register_data_2["password"]
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.delete(
            f"/user/{user_id_1}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "This user can only delete their own account.",
                                             f"Wrong error message '{response3.content}'")
