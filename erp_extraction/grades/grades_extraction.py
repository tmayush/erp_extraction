import os, urllib.parse
import requests
from erp_extraction.setup import GLOBAL_
from erp_extraction.erp_utils import util_helper
from erp_extraction.grades import grades_json, grades_csv


def get_semesters_from_html(temp_page_fp) -> dict:
    available_sems_raw = util_helper.extract_formdata(temp_page_fp, "submit")
    # available_sems = {}
    # for sem_id, sem_name in available_sems_raw.items():
    #     available_sems[urllib.parse.unquote(sem_id)] = urllib.parse.unquote(sem_name)
    # return available_sems
    return {
        urllib.parse.unquote_plus(sem_id): urllib.parse.unquote_plus(sem_name)
        for sem_id, sem_name in available_sems_raw.items()
    }


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
    print(f"{resp.status_code} status code - Can access the marks page")
    with open(temp_page_fp, "w+") as file:
        file.write(resp.text)


def create_filled_semwise_marks_page(
    sem_data: dict, cur_ses: requests.Session, url: str, file_locations: dict
):
    temp_page_fp = file_locations["temp_page_fp"]
    marks_page_fp = file_locations["marks_page_fp"]

    formdata_dict = util_helper.extract_formdata(temp_page_fp, "hidden")
    # del cur_ses.headers["Pragma"]
    # del cur_ses.headers["Cache-Control"]
    formdata_dict.update(sem_data)
    formdata = util_helper.format_formdata(formdata_dict)
    res = cur_ses.post(url, data=formdata)
    print(f"{res.status_code} status code - Generated the marks page with grades")
    with open(marks_page_fp, "w+") as file:
        file.write(res.text)


def get_semesters(cur_ses: requests.Session, marks_page_fl: dict) -> dict:
    url = "https://erp.cbit.org.in/StudentLogin/Student/OverallMarksSemwise.aspx"
    create_temp_semwise_marks_page(cur_ses, url, marks_page_fl)
    return get_semesters_from_html(marks_page_fl["temp_page_fp"])


def get_grades(sem_data, sem_num: int, cur_ses: requests.Session, marks_page_fl: dict):
    url = "https://erp.cbit.org.in/StudentLogin/Student/OverallMarksSemwise.aspx"
    user_sem_data = {
        urllib.parse.quote_plus(k): urllib.parse.quote_plus(v)
        for k, v in sem_data.items()
        if int(k[-1]) == sem_num
    }
    create_filled_semwise_marks_page(user_sem_data, cur_ses, url, marks_page_fl)
    os.remove(marks_page_fl["temp_page_fp"])
    grades_json.create_marks_db(sem_num)
    grades_csv.create_csv(sem_num)
