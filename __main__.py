import os
from erp_extraction import setup
from erp_extraction.load_erp import load_my_erp


def main():
    GLOBAL_ = setup.GLOBAL_
    os.chdir("./erp_extraction")
    cwd = os.getcwd()
    GLOBAL_["root"] = cwd
    configs_F = os.path.join(cwd, "configs")
    if not os.path.exists(configs_F):
        print("Configs folder missing, please re-install the app correctly")
        return
    config_fp = os.path.join(configs_F, "app.config.json")
    paths_fp = os.path.join(configs_F, "paths.json")
    GLOBAL_["config_data"] = setup.get_configs_data(config_fp)
    if GLOBAL_["config_data"]["first_run"]:
        GLOBAL_["config_data"]["first_run"] = False
        setup.update_configs_data(GLOBAL_["config_data"], config_fp)
        setup.main(paths_fp)
    GLOBAL_["paths"] = setup.get_configs_data(paths_fp)
    load_my_erp.main()


main()
