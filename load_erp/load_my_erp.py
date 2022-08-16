import requests, os, json
from erp_extraction.erp_utils import util_helper
from erp_extraction.erp_utils import erp_csv
from erp_extraction.erp_utils import erp_db
from erp_extraction.setup import GLOBAL_
from erp_extraction.grades import get_grades


def get_cred(cred_filepath: str) -> dict:
    """Retrieves the credentials from the credentials.json file from
    the current directory

    Args:
        GLOBAL (dict): Stores all the global variables used throughout
        the program
    """
    with open(cred_filepath) as file:
        json_data = json.loads(file.read())
    return json_data


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


def visit(
    creds: dict, session_obj: requests.Session, erp_url: str, homepage_fp: str
) -> None:
    username = creds["username"]
    password = creds["password"]

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
    formdata = util_helper.get_formatted_formdata("temp.html", "hidden")

    # Gives Username
    formdata += f"&txtUserName={username}"
    uname_visit_res = session_obj.post(erp_url, formdata)
    print(f"{uname_visit_res.status_code} - after giving username status code")

    with open("temp.html", "w+") as f:
        f.write(uname_visit_res.text)

    formdata = util_helper.get_formatted_formdata("temp.html", "hidden")
    os.remove("temp.html")

    # Gives Password
    formdata += f"&txtPassword={password}&btnSubmit=Submit"
    pwd_visit_res = session_obj.post(erp_url, formdata)
    print(f"{pwd_visit_res.status_code} - after giving password status code")

    with open(homepage_fp, "w+") as f:
        f.write(pwd_visit_res.content.decode("utf8"))

    print("Successfully Generated Homepage")


def main():
    # file locations data (dict)
    file_loc = GLOBAL_["paths"][1]
    csv_fp = file_loc["attendance_data"]
    homepage_fp = file_loc["erp_homepage"]
    creds = get_cred(file_loc["credentials"])
    url = "https://erp.cbit.org.in/beeserp/Login.aspx?ReturnUrl=%2fbeeserp%2f"
    with requests.Session() as cur_ses:
        set_headers(cur_ses)
        visit(creds, cur_ses, url, homepage_fp)
    erp_db.create_db(file_loc["json_db"], homepage_fp)
    erp_csv.generate_csv(file_loc["json_db"], csv_fp)
    # get_grades.main(cur_ses, url)


if __name__ == "__main__":
    main()
