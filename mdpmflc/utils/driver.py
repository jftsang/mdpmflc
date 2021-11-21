import re
from typing import List


def get_config_fields(src, pars_name="pars") -> List[str]:
    """Reads a source code (of a MDPM driver) and find all instances of
    'pars.at("...")', to find out all the config fields that can be read
    from a config file.
    """
    # regex = f'{pars_name}.at(".*")'
    regex = r'pars\.at\("(.*?)"\)'
    matches = re.finditer(regex, src, re.MULTILINE)

    pars_fields = []
    for matchNum, match in enumerate(matches, start=1):
        for group_ind in range(1, len(match.groups()) + 1, 2):
            if match.group(group_ind) not in pars_fields:
                pars_fields.append(match.group(group_ind))

    return pars_fields
