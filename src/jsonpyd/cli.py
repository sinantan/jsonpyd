from .jsonpyd import JsonPyd
from .util import FileHandler

from argparse import ArgumentParser
from datetime import date


class CLI:
    def __init__(self):
        self.args = self.parse_arguments()

    def parse_arguments(self):
        parser = ArgumentParser(description="JsonPyd command line arguments")

        parser.add_argument(
            "schema_path", type=str, help="Path of the referenced schema file."
        )
        parser.add_argument(
            "--apply_snake_case",
            type=bool,
            default=True,
            help="Apply snake_case to variables.",
        )
        parser.add_argument(
            "--force_optional",
            type=bool,
            default=False,
            help="Make variables optional by default.",
        )
        parser.add_argument(
            "--file_name",
            type=str,
            default=f'{date.today().strftime("%d-%m-%Y")}_schema',
            help="Name of the output file.",
        )

        return parser.parse_args()

    def run(self):
        schema = FileHandler.read_file(path=self.args.schema_path)
        options = {k: v for k, v in vars(self.args).items() if k != "schema"}
        pkg = JsonPyd(schema=schema, options=options)
        pkg.convert_to_py()


def start_cli():
    cli = CLI()
    cli.run()
