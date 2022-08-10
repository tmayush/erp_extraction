import json, csv, os


def create_db(fp) -> None:
    if os.path.exists(fp):
        return
    with open(fp, "w+") as file:
        file.write("[]")


def update_db(new_dict: dict, old_fp: str, target_fp: str) -> None:
    final_data_arr = []

    with open(old_fp, "r+") as file:
        final_data_arr = json.load(file)

    if len(final_data_arr) >= 1:
        prev_data_dict = final_data_arr[0]
        prev_data_dict["type"] = "Previous"
        if len(final_data_arr) > 1:
            final_data_arr.pop()

    final_data_arr.insert(0, new_dict)

    with open(target_fp, "w+") as file:
        json.dump(final_data_arr, file)


def fix_row(row: list, col_size, skew="left") -> list:
    if col_size < len(row):
        raise Exception("row length greater than col_size")

    extra_data_len = col_size - len(row)
    if extra_data_len == 0:
        return row

    if skew == "left":
        row += [""] * (extra_data_len)
        return row

    if skew == "right":
        extra_data = [""] * (extra_data_len)
        extra_data += row
        return extra_data


def generate_csv(data_fp, target_fp):
    data = None
    with open(data_fp, "r+") as file:
        data = json.load(file)

    with open(target_fp, "w+", newline="") as file:
        writer = csv.writer(file)
        col_size = len(data[0]["data"][0])
        for obj in data:
            rows = obj["data"]
            writer.writerow(fix_row([obj["type"], obj["date"]], col_size))
            writer.writerows(rows)
            writer.writerow(["-"] * col_size)


def main():
    update_db(
        {"type": "updated", "date": "hello", "data": ["some"]},
        "data.json",
        "data1.json",
    )

    generate_csv("data.json", "hey.csv")


if __name__ == "__main__":
    main()
