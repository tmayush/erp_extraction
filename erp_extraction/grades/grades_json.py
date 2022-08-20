import json
import bs4
from erp_extraction.setup import GLOBAL_
from erp_extraction.erp_utils.json_utils import create_JSON_data_file


class SemwiseMarksSoup:
    def __init__(self, fp, sem_num) -> None:
        self.fp = fp
        self.sem_num = sem_num
        # Create an instance of BeautifulSoup so we can use it multiple times
        with open(fp, "r+") as file:
            self.semwisemarks_soup = bs4.BeautifulSoup(file, features="html.parser")

    def get_element_by_id(self, html_element: str, element_id: str) -> bs4.element.Tag:
        # Stores the main table that wraps the attendance content
        target_element = None

        # get all tables and filter with the specific ID to get the attendance table
        all_tables = self.semwisemarks_soup.find_all(html_element)
        for table in all_tables:
            if table.get("id") == element_id:
                target_element = table

        return target_element

    @staticmethod
    def get_summary_list(main_table: bs4.element.Tag) -> list:
        all_rows = []
        for tr in main_table.find_all("tr"):
            row_data = []
            for th in tr.children:
                # stripping because some text may have new lines at its ends
                element_text = th.text.strip()
                row_data.append(element_text)

            # The following locations contain empty strings
            row_data.pop(0)
            row_data.pop(-1)
            all_rows.append(row_data)

        return all_rows

    def get_gpas(self) -> dict:
        # The text would be something like: "SGPA : X.XX", where "X.XX"
        # is the grade. So we split it by ":" and take the second part
        # and strip it to remove any leading/trailing whitespaces
        return {
            "SGPA": self.get_element_by_id("span", "ctl00_cpStud_lblSemSGPA")
            .text.split(":")[-1]
            .strip(),
            "CGPA": self.get_element_by_id("span", "ctl00_cpStud_lblSemCGPA")
            .text.split(":")[-1]
            .strip(),
        }

    def extract_grades_data(self) -> dict:
        grades_data = {}
        main_table = self.get_element_by_id("table", "ctl00_cpStud_grdSemwise")
        grades = self.get_summary_list(main_table)
        gpas = self.get_gpas()

        grades_data["semester"] = self.sem_num
        grades_data.update(gpas)
        grades_data["grades"] = grades

        return grades_data


def setup_marks_db() -> list:
    # Retrive file paths
    file_locations = GLOBAL_["paths"][1]
    marks_db_fp = file_locations["marks_db"]

    default_user_grades_data = []

    # Looping from semester 1 to 8
    for i in range(1, 9):
        sem_grades_data = {"semester": i, "CGPA": "", "SGPA": "", "grades": []}
        default_user_grades_data.append(sem_grades_data)

    # Retrive marks data from "marks database" file
    prev_marks_data = create_JSON_data_file(marks_db_fp, default_user_grades_data)
    return prev_marks_data


def extract_grades_data(fp, sem_num):
    semwisemarks_inst = SemwiseMarksSoup(fp, sem_num)
    return semwisemarks_inst.extract_grades_data()


def create_marks_db(sem_num):
    # File locations related to the generation of CSV file
    file_locations = GLOBAL_["paths"][1]
    marks_db_fp = file_locations["marks_db"]

    # Extract grades data from the HTML file
    grades_data = extract_grades_data(file_locations["erp_semwise_marks"], sem_num)

    # setup up the marks database file if it doesn't exist and retrieve data
    # or retrieve the existing data if it does exist.
    marks_data = setup_marks_db()

    # Iterate through the marks data and find the semester data object to update
    for i in range(len(marks_data)):
        semester_data = marks_data[i]
        if semester_data["semester"] == sem_num:
            marks_data[i] = grades_data
            break
    with open(marks_db_fp, "w+") as f:
        json.dump(marks_data, f)


if __name__ == "__main__":
    create_marks_db(2)
