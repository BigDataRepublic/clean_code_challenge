from typing import Callable
import os


def get_data_path_resolver(project_data_path: str = "data") -> Callable[[str], str]:
    """
    Return a method that allows for resolving a full data path given a filename
    """

    def _get_data_path(filename: str) -> str:
        return os.path.join(project_data_path, filename)

    return _get_data_path
