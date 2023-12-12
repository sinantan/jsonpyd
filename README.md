<div align="center">
  <h2>jsonpyd</h2>
  <h3>Generate related pydantic class with any json type.</h3>
  <a href="https://github.com/sinantan/jsonpyd/stargazers"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/sinantan/jsonpyd"></a>
  <a href="https://github.com/sinantan/jsonpyd/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/sinantan/jsonpyd"></a>
  <a href="https://github.com/sinantan/jsonpyd/blob/main/LICENSE"><img alt="GitHub" src="https://img.shields.io/github/license/sinantan/jsonpyd"></a>
</div>



# JsonPyd

JsonPyd is a tool that automatically generates Pydantic models from JSON schemas.

## Installation

You can easily install it via pip:

```bash
pip install jsonpyd
```

## Usage

### Terminal Usage

JsonPyd can be used as a command-line tool:

```bash
jsonpyd /path/to/schema.json --force-optional True
```

This command will generate a `.py` file containing Python classes based on the specified JSON schema. Optionally, `--force-optional` parameter can be used to make all fields in the schema optional.

## Commands

The tool's command-line interface allows you to specify options for generating Pydantic models using the following parameters:

```bash
# Specify the path to the JSON schema file
schema_path <path_to_schema>

# Option to apply snake_case to variable names
--apply_snake_case [true|false]

# Option to force all variables to be optional
--force_optional [true|false]

# Set the name for the output file, default is the current date in 'dd-mm-yyyy_schema' format
--file_name <file_name>
```

These parameters can be used to customize the behavior of the model generation to fit your project requirements.

## Usage within a Project

JsonPyd can also be used within Python files in a project:

```python
from jsonpyd import JsonPyd

my_schema = '''
{
        "id": "1NW2ZvKYlo2CPkIVYDHw",
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
    }
'''

# Create models using JsonPyd
pkg = JsonPyd(schema=my_schema, options={"force_optional": True})


# You can get Pydantic model by calling .model attribute.
pkg.model

# Or you can create .py file
pkg.convert_to_py()

```

This creates Pydantic models based on the specified JSON schema and converts them into a `.py` file.

## Features

* Automatic Model Generation: Automatically generates Pydantic models based on JSON schema.
* Optional Fields: Allows making all fields optional within a specific schema structure.
* Pydantic Integration: The generated models can leverage all features provided by Pydantic.

## Contribution and Feedback

For any contributions and feedback, please visit my GitHub page or reach me via email.
