import json
from typing import Any, Dict
from datetime import date
from pydantic import create_model, BaseModel

from .util import FileHandler

_NEWLINE = "\n"
_TAB = "    "
_GENERATED_MODEL_NAME = "GeneratedModel"

__all__ = ["JsonPyd"]


class Options(BaseModel):
    apply_snake_case: bool = True
    force_optional: bool = False
    file_name: str = f'{date.today().strftime("%d-%m-%Y")}_schema'


class JsonPyd:
    def __init__(self, schema, options={}):
        assert self.valid_json(schema), "Schema should be String JSON format."

        self.schema = json.loads(schema)
        self.options: Options = Options(**options)
        self.model: BaseModel = self.create_base_model(self.schema)
        self.raw_code: str = self.get_raw_code()

    def __repr__(self):
        return f"{self.__class__.__name__}: [{', '.join(self.schema.keys())}]"

    @classmethod
    def valid_json(cls, v) -> bool:
        try:
            json.loads(v)
            return True
        except json.JSONDecodeError:
            return False

    def create_base_model(self, schema: Dict[str, Any]) -> BaseModel:
        """
        Create a Pydantic BaseModel based on the given schema.

        Args:
            schema (Dict[str, Any]): A dictionary representing the schema structure.

        Returns:
            BaseModel: A Pydantic BaseModel generated based on the schema.
        """
        fields = {}
        for key, value in schema.items():
            if isinstance(value, dict):
                fields[key] = (self.create_base_model(value), ...)
            else:
                value_type = type(value) if value is not None else Any
                fields[key] = (value_type, value)

        return create_model(_GENERATED_MODEL_NAME, **fields)(**schema)

    def generate_code(
        self,
        data: Dict[str, Any],
        class_name: str = _GENERATED_MODEL_NAME,
    ) -> str:
        """
        Dynamically creates a Pydantic BaseModel class based on the given data.

        Args:
            data (Dict[str, Any]): A dictionary representing the fields and types for the model.
            class_name (str, optional): The name for the generated Pydantic BaseModel class. Defaults to "GeneratedModel".

        Returns:
            str: The generated Python code representing the Pydantic BaseModel class.
        """
        code = f"class {class_name}(BaseModel):{_NEWLINE}"

        for field_name, field_value in data.items():
            field_type = (
                type(field_value).__name__ if field_value is not None else "Any"
            )
            if isinstance(field_value, dict):
                nested_code = self.generate_code(
                    field_value, f"{self.snake_to_pascal(field_name)}"
                )
                variable = f"{_TAB}{field_name}: {self.snake_to_pascal(field_name)}{_NEWLINE * 2}{nested_code}"
                code += variable
            else:
                value = ""
                if self.options.force_optional:
                    field_type = f"Optional[{field_type}]"
                    value = " = None"
                variable = f"{_TAB}{field_name}: {field_type}{value}{_NEWLINE}"
                code += variable

        return code

    def get_raw_code(self) -> str:
        """
        Generate raw code based on the model dump.

        Returns:
        str: Raw code containing class definitions.
        """
        generated_code = self.generate_code(self.model.model_dump())
        generated_code = "".join(
            ["class " + i for i in generated_code.split("class ")[::-1] if i != ""]
        )
        return self.generate_imports() + _NEWLINE + generated_code

    def convert_to_py(self) -> None:
        """
        Convert generated raw code to a Python file.
        """
        return FileHandler.write_to_file(
            filename=self.options.file_name, content=self.raw_code
        )

    @staticmethod
    def generate_imports() -> str:
        """
        Generate import statements in Python syntax based on the given import map.

        Returns:
        str: String containing import statements.
        """
        import_map = {"pydantic": ["BaseModel"], "typing": ["Any", "Optional"]}
        imports = ""
        for package, items in import_map.items():
            imports += f"from {package} import {', '.join(items)}{_NEWLINE}"
        return imports

    @staticmethod
    def snake_to_pascal(word):
        """
        Convert a snake_case string to PascalCase.

        Args:
            word (str): A string in snake_case format.

        Returns:
            str: The input string converted to PascalCase.
        """
        return "".join(x.title() for x in word.split("_"))
