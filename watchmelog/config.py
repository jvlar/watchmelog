import collections
import copy
import os
from typing import Dict

import pkg_resources
import yaml
import munch


app_config = None


def _merge_dicts(base_dict: Dict, merged_dict: Dict) -> Dict:
    new_dict = copy.deepcopy(base_dict)
    for k, v in merged_dict.items():
        if (
            k in base_dict
            and isinstance(base_dict[k], dict)
            and isinstance(merged_dict[k], collections.Mapping)
        ):
            new_dict[k] = _merge_dicts(base_dict[k], merged_dict[k])
        else:
            new_dict[k] = merged_dict[k]
    return new_dict


def load_config():
    base_config_dir = pkg_resources.resource_filename(
        "watchmelog", os.path.join("resources", "config")
    )
    base_config_file = os.path.join(base_config_dir, "config.yaml")
    local_config_file = os.path.join(base_config_dir, "local.yaml")

    with open(base_config_file, mode="r") as base_config:
        config_dict = yaml.safe_load(base_config)

    if os.path.isfile(local_config_file):
        with open(local_config_file, mode="r") as local_config:
            local_config_dict = yaml.safe_load(local_config)
        config_dict = _merge_dicts(config_dict, local_config_dict)

    globals()["app_config"] = munch.munchify(config_dict)
