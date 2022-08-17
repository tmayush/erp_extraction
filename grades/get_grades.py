import os, urllib.parse
import requests
from erp_extraction.setup import GLOBAL_
from erp_extraction.erp_utils import util_helper
from erp_extraction.grades import grades_json, grades_csv


def create_temp_semwise_marks_page(
    cur_ses: requests.Session, url: str, file_locations: dict
):
    homepage_fp = file_locations["homepage_fp"]
    temp_page_fp = file_locations["temp_page_fp"]

    formdata = util_helper.extract_formdata(homepage_fp, "hidden")
    # formdata["__EVENTTARGET"] = "ctl00$cpHeader$ucStud$lnkOverallMarksSemwise"
    formdata["__EVENTTARGET"] = "ctl00%24cpHeader%24ucStud%24lnkOverallMarksSemwise"
    # formdata.pop("__LASTFOCUS")
    resp = cur_ses.post(url, json=formdata)
    print(f"{resp.status_code} - Generated the OverallMarksSemwise page")
    with open(temp_page_fp, "w+") as file:
        file.write(resp.text)


def create_filled_semwise_marks_page(
    sem_num: int, cur_ses: requests.Session, url: str, file_locations: dict
):
    temp_page_fp = file_locations["temp_page_fp"]
    marks_page_fp = file_locations["marks_page_fp"]

    formdata_dict = util_helper.extract_formdata(temp_page_fp, "hidden")
    available_sems = util_helper.extract_formdata(temp_page_fp, "submit")

    for sem_id, sem_name in available_sems.items():
        if int(sem_id[-1]) == sem_num:
            formdata_dict[sem_id] = urllib.parse.quote_plus(sem_name)
            break
    # del cur_ses.headers["Pragma"]
    # del cur_ses.headers["Cache-Control"]

    formdata = util_helper.format_formdata(formdata_dict)
    res = cur_ses.post(url, data=formdata)
    print(f"{res.status_code} - Generated the OverallMarksSemwise page with results")
    with open(marks_page_fp, "w+") as file:
        file.write(res.text)


def main(cur_ses: requests.Session, url: str, sem_num: int):
    file_locations = GLOBAL_["paths"][1]
    # File locations related to the generation of Semwise marks page
    marks_page_fl = {
        "homepage_fp": file_locations["erp_homepage"],
        "temp_page_fp": file_locations["temp"],
        "marks_page_fp": file_locations["erp_semwise_marks"],
    }
    url = (
        "https://erp.cbit.org.in/beeserp/StudentLogin/Student/OverallMarksSemwise.aspx"
    )
    create_temp_semwise_marks_page(cur_ses, url, marks_page_fl)
    create_filled_semwise_marks_page(sem_num, cur_ses, url, marks_page_fl)
    os.remove(marks_page_fl["temp_page_fp"])
    grades_json.create_marks_db(sem_num)
    grades_csv.create_csv(sem_num)


if __name__ == "__main__":
    main()
