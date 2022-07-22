import requests, os, json
from requests.structures import CaseInsensitiveDict
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


def set_headers(headers):
    """Sets the headers before sending any requests

    Args:
        headers (CaseInsensitiveDict): Stores all the headers
    """
    headers[
        "User-Agent"
    ] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    headers[
        "Accept"
    ] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    headers["Accept-Language"] = "en-US,en;q=0.5"
    # The only two headers that matter
    headers["Accept-Encoding"] = "gzip, deflate, br"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    # /The only two headers that matter
    headers["Origin"] = "https://erp.org.in"
    headers["DNT"] = "1"
    headers["Connection"] = "keep-alive"
    headers["Upgrade-Insecure-Requests"] = "1"
    headers["Sec-Fetch-Dest"] = "document"
    headers["Sec-Fetch-Mode"] = "navigate"
    headers["Sec-Fetch-Site"] = "same-origin"
    headers["Sec-Fetch-User"] = "?1"
    headers["Pragma"] = "no-cache"
    headers["Cache-Control"] = "no-cache"


def first_visit(url, headers) -> str:
    """This will be the first web request made to ERP inorder to get
    the session ID and store the cookie as a header

    Args:
        url (str): url of the ERP website
        headers (CaseInsensitiveDict): Stores all the headers

    Returns:
        str: post data passed on to the next request (providing
        username to the site)
    """

    response = requests.get(url, headers=headers)
    print(f"{response.status_code} - first visit status code")

    # Writes the first visit html data to a temporary file from
    # which the majority of the post data is extracted
    with open("temp.html", "w+") as f:
        f.write(response.content.decode("utf8"))

    # Extracting the cookie from the headers
    cookie = response.headers.get("Set-Cookie")
    cookie_stuff = cookie.split(";")
    print(cookie_stuff[0])

    # headers["Referer"] = url
    # The cookie needs to be sent by every request after the
    # first visit. so we will set the cookie to the headers
    headers["Cookie"] = cookie_stuff[0]

    # this will give us the new post data to be sent to the server
    data = util_helper.get_data("temp.html")
    return data


def giving_username(url, headers, data) -> str:
    username = GLOBAL["username"]
    data += f"&txtUserName={username}"
    resp = requests.post(url, data, headers=headers)
    print(f"{resp.status_code} - after giving username status code")

    with open("temp.html", "w+") as f:
        f.write(resp.content.decode("utf8"))

    data = util_helper.get_data("temp.html")
    os.remove("temp.html")
    return data


def giving_password(url, headers, data) -> None:
    password = GLOBAL["password"]
    data += f"&txtPassword={password}"
    resp = requests.post(url, data, headers=headers)
    print(f"{resp.status_code} - after giving password status code")

    with open("homepage.html", "w+") as f:
        f.write(resp.content.decode("utf8"))


def main():
    get_cred(GLOBAL)
    url = "https://erp.cbit.org.in/beeserp/Login.aspx?"
    "ReturnUrl=%2fbeeserp%2f"
    headers = CaseInsensitiveDict()
    set_headers(headers)
    data = first_visit(url, headers)
    data = giving_username(url, headers, data)
    giving_password(url, headers, data)


if __name__ == "__main__":
    main()
