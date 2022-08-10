import urllib.parse as url_parse


my_list = []


def trial(file_name):
    with open(file_name, "r") as file:
        for line in file:
            if '<input type="hidden"' in line:
                my_list.append(line)


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


def get_data(file_name):
    trial(file_name)
    fin_dict = {}
    for line in my_list:
        fin_dict[get_pairs(line, "name")] = get_pairs(line, "value")
    data = ""
    for (key, value) in fin_dict.items():
        data += f"{key}={value}&"
    data = data[:-1]
    return data
