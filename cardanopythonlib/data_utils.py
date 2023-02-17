# General imports
import logging
import logging.config
from typing import Union
import json
# Module imports
from collections.abc import MutableMapping


def getlogger(logger_name, level):
    MY_LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default_formatter': {
                'format': '[%(levelname)s:%(asctime)s] %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default_formatter',
            },
        },
        'loggers': {
            logger_name: {
                'handlers': ['console'],
                'level': level,
                'propagate': True
            }
        }
    }

    logging.config.dictConfig(MY_LOGGING_CONFIG)
    logger = logging.getLogger(logger_name)
    return logger


def check_nested_dicts(vals: dict):
    """
    Check if a dictionary is nested.
    """
    if any(isinstance(v, dict) for v in vals.values()):
        return True
    else:
        return False


# def flatten_dict(input_dict, deep: bool = False):
#     """
#     Reduce dictionary to only one nested level
#     """
#     output = []
#     for key, val in input_dict.items():
#         if deep:
#             try:
#                 output.extend(flatten_dict(val).items())
#             except AttributeError:
#                 output.append((key, val))
#         else:
#             try:
#                 if check_nested_dicts(val):
#                     output.extend(flatten_dict(val).items())
#                 else:
#                     output.append((key, val))
#             except AttributeError:
#                 output.append((key, val))
#     return dict(output)

def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str ='.') -> MutableMapping:
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def validate_vars(keywords: list, input_vars: dict, mandatory: bool = False) -> list:
    """
    Complementing `validate_dict` and implemented
    at `parse_inputs`.

    TO DO:
    Missing to annotate/distinguish between optional and necessary arguments
    """
    result = []
    for key, val in input_vars.items():
        try:
            assert val is not None and key in keywords
            result.append(val)
        except AssertionError:
            if mandatory:
                print(f'Provide a valid input for {key}')
                result = []
                break
            else:
                result.append(None)
                continue
    return result


def validate_dict(keywords: list, vals: Union[str, dict]) \
        -> Union[dict, list]:
    """
    Complementing `validate_vars` and implemented
    at `parse_inputs`.
    """
    from_json = {}
    if isinstance(vals, str):
        try:
            with open(vals) as f:
                from_json = json.load(f)
        except FileNotFoundError:
            try:
                from_json = json.loads(vals)
            except TypeError:
                print('Provide a valid format for JSON.')
    else:
        try:
            return [val for arg in vals for name, val in arg.items()
                    if name in keywords]
        except AttributeError:
            print('Provide a valid input')
            return from_json
    return from_json


def parse_inputs(keywords: list, fill: bool = False, *args, **kwargs):
    """
    Parse the input for Cardano objects functions.
    """
    if args:
        output = validate_dict(keywords, args[0])
        if isinstance(output, dict):
            return [val for key, val in output.items()]
        else:
            return output
    else:
        return validate_vars(keywords, kwargs, fill)


# def load_configs(vals: Union[str, dict], full_flat: bool) -> Optional[dict]:
#     """
#     Loads configuration files into a dictionary to be use for reading configs
#     """
#     if isinstance(vals, str):
#         try:
#             with open(path_utils.validate_path(vals, False)) as file:
#                 output = json.load(file)
#                 if check_nested_dicts(output):
#                     output = flatten_dict(output, full_flat)
#             return output
#         except FileNotFoundError:
#             logging.error('The provided file was not found')
#     elif isinstance(vals, dict):
#         output = vals
#         if check_nested_dicts(output):
#             output = flatten_dict(output, full_flat)
#         return output
#     else:
#         logging.error('Not supported configuration\'s input')