import json
import os


def is_JSON_serializable(fp):
    is_serializable = False
    with open(fp, "r+") as file:
        try:
            json.load(file)
            is_serializable = True
        except json.JSONDecodeError:
            print(f"File is not formatted to parse JSON content\nfilepath: {fp}")
    return is_serializable


def create_JSON_data_file(fp, default_content=[]):
    """Retrieves data from the json file if it exists, or
    it creates a new file with default content

    Args:
        fp (str): filepath of the json file to read
        default_content (list|dict, optional): any data that can be json encoded. Defaults to [].

    Raises:
        Exception: File is not formatted to parse JSON

    Returns:
        list|dict|JSON serialized data: data from the filepath provided
    """
    if os.path.exists(fp):
        if not is_JSON_serializable(fp):
            user_input = input(
                "Do you want to overwrite the content of this file with new content? (y/n): "
            )
            if not user_input.lower() == "y":
                raise Exception(f"Corrupted file at {fp}")
        else:
            with open(fp, "r+") as f:
                content = json.load(f)
            return content
    with open(fp, "w+") as f:
        json.dump(default_content, f)
    return default_content
