import bs4
from bs4 import BeautifulSoup


def get_element_by_id(
    html_filepath: str, html_element: str, element_id: str
) -> bs4.element.Tag:
    soup = None
    # Stores the main table that wraps the attendance content
    target_element = None

    with open(html_filepath, "r") as file:
        soup = BeautifulSoup(file, features="html.parser")

    # get all tables and filter with the specific ID to get the attendance table
    all_tables = soup.find_all(html_element)
    for table in all_tables:
        if table.get("id") == element_id:
            target_element = table

    return target_element


def get_summary_list(main_table: bs4.element.Tag) -> list:
    all_rows = []
    for tr in main_table.find_all("tr"):
        row_data = []
        for th in tr.children:
            # stripping because some text may have new lines at the ends
            element_text = th.text.strip()
            row_data.append(element_text)

        # The following locations contain empty strings
        row_data.pop(0)
        row_data.pop(-1)
        all_rows.append(row_data)

    return all_rows
