import os, json
from erp_extraction.erp_utils import attendance_extraction
from erp_extraction.erp_utils import erp_time
from erp_extraction.erp_utils.json_utils import create_JSON_data_file


def create_db(json_db_fp: str, homepage_fp: str) -> None:
    print(f"Extracting data from {homepage_fp}")
    main_table = attendance_extraction.get_element_by_id(
        homepage_fp, "table", "ctl00_cpStud_grdSubject"
    )
    all_rows = attendance_extraction.get_summary_list(main_table)
    updated_data = {
        "type": "Updated",
        "date": erp_time.get_formatted_date(),
        "data": all_rows,
    }
    update_db(updated_data, json_db_fp, json_db_fp)


def update_db(new_dict: dict, old_fp: str, target_fp: str) -> None:
    final_data_arr = []

    final_data_arr = create_JSON_data_file(old_fp)

    if len(final_data_arr) >= 1:
        prev_data_dict = final_data_arr[0]
        prev_data_dict["type"] = "Previous"
        if len(final_data_arr) > 1:
            final_data_arr.pop()

    final_data_arr.insert(0, new_dict)

    with open(target_fp, "w+") as file:
        json.dump(final_data_arr, file)
