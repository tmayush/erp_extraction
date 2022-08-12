import os, json
from erp_extraction.erp_utils import attendance_extraction
from erp_extraction.erp_utils import erp_time


def create_db(json_db_fp: str, homepage_fp: str) -> None:
    print(f"Extracting data from {homepage_fp}")
    main_table = attendance_extraction.get_element_by_id(
        homepage_fp, "table", "ctl00_cpStud_grdSubject"
    )
    all_rows = attendance_extraction.get_summary_list(main_table)
    create_db_file(json_db_fp)
    updated_data = {
        "type": "Updated",
        "date": erp_time.get_formatted_date(),
        "data": all_rows,
    }
    update_db(updated_data, json_db_fp, json_db_fp)


def create_db_file(fp) -> None:
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
