from __future__ import annotations

from jsonpyd import JsonPyd


class TestJsonPyd:
    def setup_method(self):
        self.sample_data = """{
        "id": "1NWo202eZvKYlo2CPkIVYDHw",
        "object": "payment_method",
        "price": 35.5312,
        "price_str": null,
        "billing_details": {
            "address": {
                "city": null,
                "country": "TR",
                "line1": null
            },
            "email": "jenny@example.com"
        }
    }"""
        self.json_pyd = JsonPyd(self.sample_data)

    def test_repr(self):
        assert (
            repr(self.json_pyd)
            == "JsonPyd: [id, object, price, price_str, billing_details]"
        )

    def test_valid_json_true(self):
        assert self.json_pyd.valid_json('{"test": "data"}') is True

    def test_valid_json_false(self):
        assert self.json_pyd.valid_json("invalid_json_data") is False

    def test_generate_code(self):
        data = {
            "name": "John",
            "age": 30,
            "address": {"city": "New York", "zipcode": 10001},
        }
        expected = (
            "class GeneratedModel(BaseModel):\n"
            "    name: str\n"
            "    age: int\n"
            "    address: Address\n\n"
            "class Address(BaseModel):\n"
            "    city: str\n"
            "    zipcode: int\n"
        )
        assert self.json_pyd.generate_code(data) == expected

    def test_generate_imports(self):
        expected = (
            "from pydantic import BaseModel\n" "from typing import Any, Optional\n"
        )
        assert self.json_pyd.generate_imports() == expected

    def test_snake_to_pascal(self):
        assert self.json_pyd.snake_to_pascal("snake_case_string") == "SnakeCaseString"


# def generate():
#     data = """{
#         "id": "1NWo202eZvKYlo2CPkIVYDHw",
#         "object": "payment_method",
#         "price": 35.5312,
#         "price_str": null,
#         "billing_details": {
#             "address": {
#                 "city": null,
#                 "country": "TR",
#                 "line1": null
#             },
#             "email": "jenny@example.com"
#         }
#     }"""
#     pkg = JsonPyd(schema=data, options={"force_optional": True})
#     pkg.convert_to_py()
