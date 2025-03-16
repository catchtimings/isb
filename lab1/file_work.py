import json


def read_txt(directory: str) -> str:
    """
    The function opens a text file and reads the data into a string
    :param directory: file directory
    :return: string with text
    """
    try:
        with open(directory, mode="r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as fne:
        raise FileNotFoundError(f"File was not found: {fne}")
    except Exception as e:
        raise Exception(f"An error occurred when opening the file: {e}")


def save_txt(directory: str, data: str) -> None:
    """
    The function opens/creates a text file and writes data to it
    :param directory: file directory
    :param data: data that will be written to the file
    :return: None
    """
    try:
        with open(directory, mode="w", encoding="utf-8") as file:
            file.write(data)
    except Exception as e:
        raise Exception(f"An error occurred when saving the file: {e}")


def read_json(directory: str) -> dict[str, str]:
    """
    The function opens a json file and reads the key as a dictionary
    :param directory: json file directory
    :return: key as a dictionary
    """
    try:
        with open(directory, mode="r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as fne:
        raise FileNotFoundError(f"File was not found: {fne}")
    except json.JSONDecodeError as jde:
        raise ValueError(f"Error decoding the json file: {jde}")
    except Exception as e:
        raise Exception(f"An error occurred when opening the file {e}")


def save_json(directory: str, data: dict[str, str]) -> None:
    """
    The function saves the data to a json file
    :param directory: json file directory
    :param data: data that will be written to the file
    :return:
    """
    try:
        with open(directory, mode="w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
    except Exception as e:
        raise Exception(f"An error occurred when saving the file: {e}")
