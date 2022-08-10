import os
import setup
from load_erp import load_my_erp

GLOBAL_ = {}


def main():
    cwd = os.getcwd()
    GLOBAL_["root"] = cwd
    configs_F = f"{cwd}\\configs"
    config_fp = f"{configs_F}\\app.config.json"
    if not os.path.exists(configs_F):
        print("Configs folder missing, please re-install the app correctly")
        return
    GLOBAL_["config_data"] = setup.get_configs_data(config_fp)
    if GLOBAL_["config_data"]["first_run"]:
        GLOBAL_["config_data"]["first_run"] = False
        setup.main(GLOBAL_, configs_F)
    else:
        load_my_erp.main()
