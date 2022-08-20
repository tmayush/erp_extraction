from erp_extraction.setup import GLOBAL_
from erp_extraction.load_erp import load_my_erp
from erp_extraction.grades import grades_extraction
from erp_extraction.erp_utils import erp_db, erp_csv
from erp_extraction.menu import phase_00_functions as p0, phase_02_functions as p2


def attendance_summary(menu0):
    load_my_erp.main()
    file_loc = GLOBAL_["paths"][1]
    csv_fp = file_loc["attendance_data"]
    homepage_fp = file_loc["erp_homepage"]
    erp_db.create_db(file_loc["json_db"], homepage_fp)
    erp_csv.generate_csv(file_loc["json_db"], csv_fp)


def day_day_attendance(menu0):
    print("Feature not available yet :(")
    print("Work in progress")


def grades(menu0):
    file_locations = GLOBAL_["paths"][1]
    # File locations related to the generation of Semwise marks page
    marks_page_fl = {
        "homepage_fp": file_locations["erp_homepage"],
        "temp_page_fp": file_locations["temp"],
        "marks_page_fp": file_locations["erp_semwise_marks"],
    }

    if "cur_ses" not in GLOBAL_:
        load_my_erp.main()
    cur_ses = GLOBAL_["cur_ses"]
    sem_data = grades_extraction.get_semesters(cur_ses, marks_page_fl)
    menu0.__p0grades_sem_data = sem_data

    print("Choose the semester to fetch grades from")
    p1_options = {semester: p2.get_grades_from_sem for semester in sem_data.values()}
    menu0.add_phase("choose_semester", p1_options)
    menu0.set_current_menu_id("choose_semester")
