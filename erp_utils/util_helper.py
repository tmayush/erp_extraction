import urllib.parse as url_parse


def filter_input_tag(fp, input_type) -> list:
    input_lines = []
    with open(fp, "r") as file:
        for line in file:
            if f'<input type="{input_type}"' in line:
                input_lines.append(line)
    return input_lines


def get_pairs(line, attr):
    full_attr = f'{attr}="'
    res = line.find(full_attr) + len(full_attr)
    content = ""
    while res < (len(line) - 1):
        char = line[res]
        if char == '"':
            break
        content += char
        res += 1

    # url encoded string
    return url_parse.quote(content, safe="")


def get_formatted_formdata(fp, input_type) -> str:
    """_summary_

    Args:
        fp (str): filepath of the file to extract data from
        input_type (str): html input type to target, to extract the control names and values

    Returns:
        str: POST data
    """
    formdata_dict = extract_formdata(fp, input_type)
    return format_formdata(formdata_dict)


def format_formdata(formdata: dict) -> str:
    data = ""
    for (control_name, value) in formdata.items():
        data += f"{control_name}={value}&"
    data = data[:-1]
    return data


def extract_formdata(fp, input_type) -> dict:
    input_lines = filter_input_tag(fp, input_type)
    fin_dict = {}
    for line in input_lines:
        fin_dict[get_pairs(line, "name")] = get_pairs(line, "value")
    return fin_dict
