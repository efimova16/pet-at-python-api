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
