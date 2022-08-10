import os, json

GLOBAL_ = {}


def get_configs_data(config_fp) -> dict:
    """Could be app.config.json file or file_locations.json data

    Args:
        config_fp (str): filepath of the config file

    Returns:
        dict: Contains the configs for the given instance
    """
    data = {}
    with open(config_fp, "r+") as file:
        data = json.load(file)
    return data


def update_configs_data(data, config_fp) -> None:
    with open(config_fp, "w+") as file:
        json.dump(data, file)


def touch(path) -> None:
    with open(path, "a"):
        os.utime(path, None)


def setup_entities(fl_fp) -> None:
    locations = []
    with open(fl_fp, "r+") as file:
        locations = json.load(file)

    for location_type in locations:
        for key, value in location_type.items():
            if key == "app_root":
                continue
            elif key[-2:] == "_F":
                if not os.path.exists(value):
                    os.mkdir(value)
            else:
                touch(value)


def create_fl_config(fp, root) -> None:
    folder_loc_data = {
        "app_root": root,
        "internal_F": f"{root}\\internal_data",
        "attendance_data_F": f"{root}\\attendance data",
    }
    file_loc_data = {
        "credentials": folder_loc_data["internal_F"] + "\\credentials.json",
        "json_db": folder_loc_data["internal_F"] + "\\data.json",
        "attendance_data": folder_loc_data["attendance_data_F"]
        + "\\attendance data.csv",
        "erp_homepage": folder_loc_data["internal_F"] + "\\homepage.html",
    }
    with open(fp, "w+") as file:
        json.dump([folder_loc_data, file_loc_data], file)


def main(configs_F):
    cwd = GLOBAL_["root"]
    file_locations = f"{configs_F}\\file_locations.json"
    user_input = None
    file_locations_exists = os.path.exists(file_locations)
    if file_locations_exists:
        user_input = input(
            "File locations config already exists. Do you want to use those "
            "configs or overwrite with the default configs (y/n)\n"
        )
    if user_input == "y" or not file_locations_exists:
        create_fl_config(file_locations, cwd)

    # Create file locations
    setup_entities(file_locations)


if __name__ == "__main__":
    main()
