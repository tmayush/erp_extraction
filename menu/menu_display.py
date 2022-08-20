import erp_extraction.menu.phase_00_functions as p0
import erp_extraction.menu.phase_01_functions as p1


class Menu:
    menu_id = "start"
    last_user_input = None
    __phases = [
        {
            "id": "start",
            "options": {
                "Attendance Summary": p1.attendance_summary,
                "Day to Day Attendance Table": p1.day_day_attendance,
                "Grades": p1.grades,
                "Exit": p0.exitmenu,
            },
        }
    ]

    def __init__(self) -> None:
        pass

    def get_options(self):
        for phase in self.__phases:
            if phase["id"] == self.get_current_menu_id():
                return phase["options"]

    def add_phase(self, id, options):
        self.__phases.append({"id": id, "options": options})

    def display_menu(self):
        while True:
            print("\n")
            cur_id = self.get_current_menu_id()
            if cur_id == "end":
                break

            options = self.get_options()

            for (index, option) in enumerate(options.keys()):
                print(f"{index + 1}. {option}")

            print()
            user_input = int(input("Option: ")) - 1
            self.last_user_input = user_input
            print()
            for (index, cb) in enumerate(options.values()):
                # From python 3.6+ disctionaries are ordered
                if index == user_input:
                    cb(self)

    def get_current_menu_id(self):
        return self.menu_id

    def set_current_menu_id(self, new_id):
        self.menu_id = new_id
