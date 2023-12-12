__all__ = ["FileHandler"]


class FileHandler:
    """
    A utility class for file handling operations.
    """

    @staticmethod
    def _perform_file_operation(filename: str, mode: str, content: str = None):
        """
        Perform a file operation (e.g., create, write) based on the specified mode.

        Args:
            filename (str): The name of the file to perform the operation on.
            mode (str): The mode for file operation ('w' for write, 'r' for read, etc.).
            content (str, optional): The content to be written to the file (for 'w' mode). Defaults to None.

        Raises:
            FileNotFoundError: If the specified file is not found.
            Exception: For any other unforeseen exceptions during file operations.
        """
        mappings = {"w": "write", "r": "read"}
        try:
            with open(filename, mode) as file:
                return getattr(file, mappings.get(mode))(content)
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise e

    @staticmethod
    def create_file(filename: str) -> None:
        """
        Create a new file with the given filename.

        Args:
            filename (str): The name of the file to create.
        """
        FileHandler._perform_file_operation(filename, "w")

    @staticmethod
    def read_file(path: str):
        """
        Read a file with the given path.

        Args:
            path (str): The path of the file to read.
        """
        return FileHandler._perform_file_operation(path, "r")

    @staticmethod
    def write_to_file(filename: str, content: str, file_type: str = "py") -> None:
        """
        Write content to a file with the given filename and file type.

        Args:
            filename (str): The name of the file to write to.
            content (str): The content to be written to the file.
            file_type (str, optional): The type of the file to create. Defaults to "py".
        """
        FileHandler._perform_file_operation(f"{filename}.{file_type}", "w", content)
