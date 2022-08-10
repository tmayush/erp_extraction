import os
from erp_extraction import setup
from erp_extraction.load_erp import load_my_erp


def main():
    GLOBAL_ = setup.GLOBAL_
    os.chdir("./erp_extraction")
    cwd = os.getcwd()
    GLOBAL_["root"] = cwd
    configs_F = f"{cwd}\\configs"
    config_fp = f"{configs_F}\\app.config.json"
    fl_fp = f"{configs_F}\\file_locations.json"
    if not os.path.exists(configs_F):
        print("Configs folder missing, please re-install the app correctly")
        return
    GLOBAL_["config_data"] = setup.get_configs_data(config_fp)
    if GLOBAL_["config_data"]["first_run"]:
        GLOBAL_["config_data"]["first_run"] = False
        setup.update_configs_data(GLOBAL_["config_data"], config_fp)
        setup.main(configs_F)
    GLOBAL_["file_locations"] = setup.get_configs_data(fl_fp)
    load_my_erp.main()


main()
