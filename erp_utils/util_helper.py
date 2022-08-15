import urllib.parse as url_parse


def filter_input_tag(file_name, input_type):
    input_lines = []
    with open(file_name, "r") as file:
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


def get_formatted_formdata(file_name, input_type):
    formdata_dict = get_formdata(file_name, input_type)
    data = ""
    for (key, value) in formdata_dict.items():
        data += f"{key}={value}&"
    data = data[:-1]
    return data


def get_formdata(file_name, input_type) -> dict:
    input_lines = filter_input_tag(file_name, input_type)
    fin_dict = {}
    for line in input_lines:
        fin_dict[get_pairs(line, "name")] = get_pairs(line, "value")
    return fin_dict
