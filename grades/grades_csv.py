import csv, json
from erp_extraction.setup import GLOBAL_
from erp_extraction.erp_utils.erp_csv import fix_row


def create_csv(sem_num):
    # File locations related to the generation of CSV file
    file_locations = GLOBAL_["paths"][1]
    marks_db_fp = file_locations["marks_db"]

    marks_data = None
    needed_marks_data = None
    user_grades_data = []

    # get marks data from database
    with open(marks_db_fp, "r+") as file:
        marks_data = json.load(file)

    # Iterate through and find the semester data object to update
    for semester_data in marks_data:
        if semester_data["semester"] == sem_num:
            needed_marks_data = semester_data
            break

    col_size = len(needed_marks_data["grades"][0])

    # append all grades data to user_grades_data
    for grade in needed_marks_data["grades"]:
        user_grades_data.append(grade)

    # Add a seperator between the grades data and the metadata/other info
    # which will be added after this statement
    user_grades_data.append(fix_row(["-"] * col_size, col_size))
    user_grades_data.append(
        fix_row(["Semester", needed_marks_data["semester"]], col_size)
    )
    user_grades_data.append(fix_row(["SGPA", needed_marks_data["SGPA"]], col_size))
    user_grades_data.append(fix_row(["CGPA", needed_marks_data["CGPA"]], col_size))

    # write the formatted list to the CSV file
    with open(file_locations["marks_data"], "w+", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(user_grades_data)


if __name__ == "__main__":
    create_csv()
