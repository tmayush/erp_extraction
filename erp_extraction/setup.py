import os, json

GLOBAL_ = {}


def ask_credentials(creds_fp):
    print(
        f"Your credentials are stored locally at {creds_fp} and "
        "are not sent to any external server other than erp.cbit.org.in"
    )
    print("Please enter your credentials: ")
    creds = {"username": input("username: "), "password": input("password: ")}
    with open(creds_fp, "w+") as file:
        json.dump(creds, file)


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
        "internal_F": os.path.join(root, "internal_data"),
        "user_data_F": os.path.join(root, "user data"),
    }
    internal_F_fp = folder_loc_data["internal_F"]
    user_data_F_fp = folder_loc_data["user_data_F"]
    file_loc_data = {
        "credentials": os.path.join(internal_F_fp, "credentials.json"),
        "json_db": os.path.join(internal_F_fp, "data.json"),
        "marks_db": os.path.join(internal_F_fp, "marks_db.json"),
        "erp_homepage": os.path.join(internal_F_fp, "homepage.html"),
        "erp_semwise_marks": os.path.join(internal_F_fp, "erp_semwise_marks.html"),
        "attendance_data": os.path.join(user_data_F_fp, "attendance data.csv"),
        "marks_data": os.path.join(user_data_F_fp, "marks data.csv"),
        "temp": os.path.join(internal_F_fp, "temp.html"),
    }
    with open(fp, "w+") as file:
        json.dump([folder_loc_data, file_loc_data], file)


def main(paths_fp):
    cwd = GLOBAL_["root"]
    user_input = None
    paths_fp_exists = os.path.exists(paths_fp)
    if paths_fp_exists:
        user_input = input(
            "File locations config already exists. Do you want to use those "
            "configs or overwrite with the default configs (y/n)\n"
        )
    if user_input == "y" or not paths_fp_exists:
        create_fl_config(paths_fp, cwd)

    # Create file locations
    setup_entities(paths_fp)


if __name__ == "__main__":
    main()
