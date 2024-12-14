import allure

from src.assertions import Assertions
from src.base_case import BaseCase
from src.my_requests import MyRequests


@allure.epic("Edit user cases")
class TestUserEdit(BaseCase):
    @allure.feature("Positive cases")
    @allure.title("Edit just created user")
    def test_edit_just_created_user(self):
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

        new_name = "changed"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 200)

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        Assertions.assert_code_status(response4, 200)
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "Wrong name after edit")

    @allure.feature("Negative cases")
    @allure.title("Edit data without authorization")
    def test_edit_data_without_auth(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")
        user_id = self.get_json_value(response1, "id")

        new_name = "changed"
        response2 = MyRequests.put(f"/user/{user_id}", data={"firstName": new_name})
        Assertions.assert_code_status(response2, 400)
        Assertions.assert_json_value_by_name(response2, "error", "Auth token not supplied",
                                             f"Wrong error message '{response2.content}'")

    @allure.feature("Negative cases")
    @allure.title("Edit user data with other user auth data")
    def test_edit_user_with_other_auth_data(self):
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

        new_name = "changed"
        response3 = MyRequests.put(
            f"/user/{user_id_1}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "This user can only edit their own data.",
                                             f"Wrong error message '{response2.content}'")

    @allure.feature("Negative cases")
    @allure.title("Edit data with wrong email format")
    def test_edit_data_with_wrong_email_format(self):
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

        new_email = "changed.email"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"email": new_email}
        )
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "Invalid email format",
                                             f"Wrong error message '{response2.content}'")

    @allure.feature("Negative cases")
    @allure.title("Edit data with short 'userName' value")
    def test_edit_with_short_username_value(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        self.auth_sid = self.get_cookie(response2, "auth_sid")
        self.token = self.get_header(response2, "x-csrf-token")

        new_name = "A"
        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid},
            data={"firstName": new_name}
        )
        Assertions.assert_code_status(response3, 400)
        Assertions.assert_json_value_by_name(response3, "error", "The value for field `firstName` is too short",
                                             f"Wrong error message '{response2.content}'")
