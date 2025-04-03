import json


def read_data(directory: str) -> str | dict[str, str]:
    try:
        with open(directory, mode="r", encoding="utf-8") as file:
            if directory.endswith(".json"):
                return json.load(file)
            else:
                return file.read()
    except FileNotFoundError as fe:
        raise FileNotFoundError(f"File was not found: {fe}")
    except json.JSONDecodeError as jde:
        raise ValueError(f"Error decoding the json file: {jde}")
    except Exception as e:
        raise Exception(f"An error occurred when opening the file {e}")