"""
Utils submodule related with path and files on system
"""

import json
import logging
import os
import shutil
# General imports
import sys
from configparser import ConfigParser
from pathlib import Path
from typing import Union, Any


def get_root_path() -> str:
    """
    Set working directory for project root independently of runner device

    Returns
    ------
    working_dir: str
        Full path to working directory
    """
    root_dir_name = 'CardanoPython'
    root_path = ''
    path_list = str(Path(__file__)).split('/')
    index = 0
    for d in path_list:
        if d != root_dir_name:
            root_path += d + '/'
            index += 1
        else:
            if (path_list[index + 1] == root_dir_name):
                root_path += d + '/'
                break
            else:
                break
    return root_path + root_dir_name


def set_working_path(target_paths: Union[str, list]) -> None:
    """
    Add to path the target routes passed down which are also included inside
    the repository folder

    Parameters
    ----------
    target_paths: Union[str, list], default=None
        Folder(s) and/or file(s) to be included in path.
        When default, still appends root directory to path.
    """
    working_dir = get_root_path()
    if isinstance(target_paths, list):
        for t_path in target_paths:
            n_dir = f'{working_dir}/{t_path}'
            sys.path.insert(0, n_dir)
    elif isinstance(target_paths, str):
        n_dir = f'{working_dir}/{target_paths}'
        sys.path.insert(0, n_dir)
    else:
        sys.path.insert(0, working_dir)


def join_paths(left_side: str, right_side: str):
    """
    Join to parts of a path
    """
    n_left = '/'.join(left_side.split('/')[:-1]) \
        if left_side.split('/')[-1] == '' else left_side
    n_right = '/'.join(right_side.split('/')[1:]) \
        if right_side.split('/')[0] == '.' else right_side
    return f"{n_left}/{n_right}"


def validate_path(input_path: str, use_root: bool = False, exists: bool = False) -> str:
    """
    Turn a relative path into an absolute one or returns one path that could
    be left joined with a parent path
    """
    if input_path.split('/')[0] == '.' or input_path.split('/')[0] == '..':
        if use_root and exists:
            return _find_path(get_root_path(), '/'.join(input_path.split('/')[1:]))
        elif use_root and not exists:
            return join_paths(get_root_path(), '/'.join(input_path.split('/')[1:]))
        else:
            return '/'.join(input_path.split('/')[1:])
    else:
        if use_root and exists:
            return _find_path(get_root_path(), input_path)
        elif use_root and not exists:
            return join_paths(get_root_path(), input_path)
        else:
            return input_path


def _find_path(starting_path: str, target_path: str) -> str:
    # To-do: It needs to verify if the starting_path is not already contain
    # in the target path before going trough os.listdir()
    try:
        if target_path.split('/')[0] not in os.listdir(starting_path):
            new_start = f"{starting_path}/{target_path.split('/')[0]}"
            _find_path(new_start, '/'.join(target_path.split('/')[1:]))
        return f"{starting_path}/{target_path}"
    except IndexError:
        raise KeyError("The provided path was not found in the Library folder")


def only_folder_path(input_str: str) -> str:
    """
    Validate if an inputed path is a folder. If it is a file
    it cuts it down to its parent
    """
    return input_str if len(input_str.split('/')[-1].split('.')) == 1\
        else '/'.join(input_str.split('/')[:-1])


def create_folder(target_path: Union[str, list]) -> None:
    """
    Creates a folder in the indicated path(s)

    Parameters
    ----------
    target_path: Union[str, list]
        Individual or list of path to folders to be created
    """
    if isinstance(target_path, list):
        for t_path in target_path:
            only_folder = only_folder_path(t_path)
            if not os.path.exists(only_folder):
                os.makedirs(only_folder)
                logging.info("Folder created at `%s`", only_folder)
            else:
                logging.info("Folder `%s` already exists", only_folder)
    else:
        only_folder = only_folder_path(target_path)
        if not os.path.exists(only_folder):
            os.makedirs(only_folder)
            logging.info("Folder created at `%s`", only_folder)
        else:
            logging.info("Folder `%s` already exists", only_folder)


def remove_folder(target_path: Union[str, list]) -> None:
    """
    Deletes folder at system level

    Parameters
    ---------
    target_path: Union[str, list]
        Individual or list of path to folders to be deleted
    """
    if isinstance(target_path, list):
        for t_path in target_path:
            only_folder = only_folder_path(t_path)
            if os.path.exists(only_folder):
                shutil.rmtree(only_folder)
                logging.info("Folder removed at %s", only_folder)
            else:
                logging.info("Folder %s did not exists", only_folder)
    else:
        only_folder = only_folder_path(target_path)
        if os.path.exists(only_folder):
            shutil.rmtree(only_folder)
            logging.info("Folder removed at %s", only_folder)
        else:
            logging.info("Folder %s did not exists", only_folder)


def file_exists(target_path: Union[str, list], is_absolute: bool = False) \
        -> Union[bool, list]:
    """
    Verify wether a file exists or not
    """
    if isinstance(target_path, str):
        if is_absolute:
            return os.path.exists(target_path)
        else:
            return os.path.exists(validate_path(target_path, True))
    else:
        if is_absolute:
            return [os.path.exists(p) for p in target_path]
        else:
            return [os.path.exists(validate_path(p, True))
                    for p in target_path]


def save_file(target_path: str, file_name: str, content: str) -> None:
    """
    Saves strings to a file specified by inputed path
    """
    create_folder(target_path)
    with open(target_path+file_name, 'w') as file:
        file.write(str(content))


def remove_file(path: str, name: str) -> None:
    if os.path.exists(path+name):
        os.remove(path+name)

def save_metadata(path: str, file_name: str, metadata: Any):
    create_folder(path)
    if metadata == {}:
        metadata_json_file = ''
    else:
        with open(path + '/' + file_name, 'w') as file:
            json.dump(metadata, file, indent=4, ensure_ascii=False)
        metadata_json_file = path + '/' + file_name

    return metadata_json_file

def config(config_path, section):
    # create a parser
    parser=ConfigParser()
    # read config file
    parser.read(config_path)
    params = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            params[item[0]] =item[1]

    else:
        raise Exception('Section {0} not found in the {1} file'.format(section,config_path))
    
    return params