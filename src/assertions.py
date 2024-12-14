import json

from requests import Response


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_msg):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response '{response.text}' is not JSON"

        assert name in response_as_dict, f"No '{name}' key in response"
        assert response_as_dict[name] == expected_value, f"{error_msg}. Actual value is '{response_as_dict[name]}'"

    @staticmethod
    def assert_json_has_key(response: Response, key):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response '{response.text}' is not JSON"

        assert key in response_as_dict, f"No '{key}' key in response"

    @staticmethod
    def assert_json_has_keys(response: Response, keys: list):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response '{response.text}' is not JSON"

        for key in keys:
            assert key in response_as_dict, f"No '{key}' key in response"

    @staticmethod
    def assert_json_has_not_key(response: Response, key):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f"Response '{response.text}' is not JSON"

        assert key not in response_as_dict, f"There is  '{key}' key in response"

    @staticmethod
    def assert_code_status(response: Response, exp_code):
        assert response.status_code == exp_code, \
            f"Unexpected status code '{response.status_code}'. Expected status code is '{exp_code}'."
