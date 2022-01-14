from typing import List


def remove_punctuation(text: str) -> List[str]:
    """
    Cleans text by seperating all the words and removing punctuation.
    """
    str_list = [
        "".join(character for character in chunk if character.isalnum())
        for chunk in text.split()
    ]
    str_list = [str.lower() for str in str_list]
    return str_list
