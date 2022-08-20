"""Common functions that are useful for multiple phases.

Should not depend on any other phases
"""


def exitmenu(menu0):
    """Sets the cuurent menu id to the "end" phase

    Args:
        menu0 (menu_display.Menu): Instance of the Menu class
    """
    menu0.set_current_menu_id("end")


def startmenu(menu0):
    menu0.set_current_menu_id("start")
