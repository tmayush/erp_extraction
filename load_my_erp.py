import requests, os, json
import util_helper
import utils.attendance_extraction as attendance
import utils.json_csv_util as jcv
from utils import time_util


GLOBAL = {}


def get_cred(GLOBAL: dict, cred_filepath: str) -> None:
    """Retrieves the credentials from the credentials.json file from
    the current directory

    Args:
        GLOBAL (dict): Stores all the global variables used throughout
        the program
    """
    with open(cred_filepath) as file:
        json_data = json.loads(file.read())
        GLOBAL["username"] = json_data["username"]
        GLOBAL["password"] = json_data["password"]


def set_headers(session_obj: requests.Session) -> None:
    """Sets the headers before sending any requests

    Args:
        session_obj (requests.Session): session object for the current
        session
    """
    injected_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        # The only two headers that matter
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        # /The only two headers that matter
        "Origin": "https://erp.cbit.org.in",
        "Host": "erp.cbit.org.in",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }
    session_obj.headers.update(injected_headers)


def visit(session_obj: requests.Session, erp_url: str, homepage_filepath: str) -> None:
    username = GLOBAL["username"]
    password = GLOBAL["password"]

    # First Visit
    # This will be the first web request made to ERP inorder to get
    # the session ID and store it as a cookie
    first_visit_res = session_obj.get(erp_url)
    print(f"{first_visit_res.status_code} - first visit status code")

    # Writes the first visit html data to a temporary file from
    # which the majority of the post data is extracted
    with open("temp.html", "w+") as file:
        file.write(first_visit_res.text)

    # this will give us the new post data to be sent to the server
    data = util_helper.get_data("temp.html")

    # Gives Username
    data += f"&txtUserName={username}"
    uname_visit_res = session_obj.post(erp_url, data)
    print(f"{uname_visit_res.status_code} - after giving username status code")

    with open("temp.html", "w+") as f:
        f.write(uname_visit_res.text)

    data = util_helper.get_data("temp.html")
    os.remove("temp.html")

    # Gives Password
    data += f"&txtPassword={password}"
    pwd_visit_res = session_obj.post(erp_url, data)
    print(f"{pwd_visit_res.status_code} - after giving password status code")

    with open(homepage_filepath, "w+") as f:
        f.write(pwd_visit_res.content.decode("utf8"))

    print("Successfully Generated Homepage")


def createcsv(csv_filepath: str, homepage_fp: str) -> None:
    print(f"Extracting data from {homepage_fp}")
    main_table = attendance.get_element_by_id(
        homepage_fp, "table", "ctl00_cpStud_grdSubject"
    )
    all_rows = attendance.get_summary_list(main_table)
    json_file = "data.json"
    jcv.create_db(json_file)
    my_dict = {
        "type": "Updated",
        "date": time_util.get_formatted_date(),
        "data": all_rows,
    }
    jcv.update_db(my_dict, json_file, json_file)
    jcv.generate_csv(json_file, csv_filepath)
    print(f"Generated a CSV file - {csv_filepath}")


def main():
    csv_file_path = "attendance.csv"
    homepage_file_path = "homepage.html"
    get_cred(GLOBAL, "credentials.json")
    url = "https://erp.cbit.org.in/beeserp/Login.aspx?ReturnUrl=%2fbeeserp%2f"
    with requests.Session() as cur_ses:
        set_headers(cur_ses)
        visit(cur_ses, url, homepage_file_path)

    createcsv(csv_file_path, homepage_file_path)


if __name__ == "__main__":
    main()
