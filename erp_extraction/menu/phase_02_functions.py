from erp_extraction.setup import GLOBAL_
from erp_extraction.grades import grades_extraction
from erp_extraction.menu import phase_00_functions as p0

# from erp_extraction.menu.menu_display import Menu


def get_grades_from_sem(menu0):
    file_locations = GLOBAL_["paths"][1]
    # File locations related to the generation of Semwise marks page
    marks_page_fl = {
        "homepage_fp": file_locations["erp_homepage"],
        "temp_page_fp": file_locations["temp"],
        "marks_page_fp": file_locations["erp_semwise_marks"],
    }

    sem_num = int(menu0.last_user_input) + 1

    grades_extraction.get_grades(
        menu0.__p0grades_sem_data, sem_num, GLOBAL_["cur_ses"], marks_page_fl
    )

    p0.startmenu(menu0)
