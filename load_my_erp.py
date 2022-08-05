import requests, os, json
import util_helper

GLOBAL = {}


def get_cred(GLOBAL) -> None:
    """Retrieves the credentials from the credentials.json file from
    the current directory

    Args:
        GLOBAL (dict): Stores all the global variables used throughout
        the program
    """
    with open("credentials.json") as file:
        json_data = json.loads(file.read())
        GLOBAL["username"] = json_data["username"]
        GLOBAL["password"] = json_data["password"]


def set_headers(session_obj: requests.Session):
    """Sets the headers before sending any requests

    Args:
        headers (CaseInsensitiveDict): Stores all the headers
    """
    injected_headers = {
        # "Cookie": "_pbjs_userid_consent_data",
        "User-Agent": "hello",
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


def visit(session_obj: requests.Session, erp_url: str):
    # session_obj = requests.Session()
    username = GLOBAL["username"]
    password = GLOBAL["password"]

    # First Visit
    # This will be the first web request made to ERP inorder to get
    # the session ID and store it as a cookie
    erp_res = session_obj.get(erp_url)
    print(f"{erp_res.status_code} - first visit status code")

    # Writes the first visit html data to a temporary file from
    # which the majority of the post data is extracted
    with open("temp.html", "w+") as file:
        file.write(erp_res.text)

    # this will give us the new post data to be sent to the server
    data = util_helper.get_data("temp.html")

    # Gives Username
    data += f"&txtUserName={username}"
    resp = session_obj.post(erp_url, data)
    print(f"{resp.status_code} - after giving username status code")

    with open("temp.html", "w+") as f:
        f.write(resp.text)

    data = util_helper.get_data("temp.html")
    os.remove("temp.html")

    # Gives Password
    data += f"&txtPassword={password}"
    resp = session_obj.post(erp_url, data)
    print(f"{resp.status_code} - after giving password status code")

    with open("homepage.html", "w+") as f:
        f.write(resp.content.decode("utf8"))

    print("Successfully Generated Homepage")


def main():
    get_cred(GLOBAL)
    url = "https://erp.cbit.org.in/beeserp/Login.aspx?"
    "ReturnUrl=%2fbeeserp%2f"
    with requests.Session() as cur_ses:
        set_headers(cur_ses)
        visit(cur_ses, url)


if __name__ == "__main__":
    main()
