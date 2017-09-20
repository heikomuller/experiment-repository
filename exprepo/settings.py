"""Everything related to configuration settings."""

import os
import yaml

from exprepo import REPO_DIR, SETTINGS_FILE


def get_setting(config, para):
    """Return the value that is associated with the given parameter expression.
    The expression can be a path expression.

    Raises ValueError if the specified parameter does not exist or references an
    internal document in the nested configuration document.

    Parameters
    ----------
    config: dict()
        Dictionary of configuration settings
    para: string
        Configuration parameter expression

    Returns
    -------
    string
    """
    el = config
    for comp in para.split('/'):
        if isinstance(el, dict):
            if comp in el:
                el = el[comp]
            else:
                raise ValueError('unknown parameter \'' + para + '\'')
        else:
            raise ValueError('cannot get value of \'' + para + '\'')
    if not isinstance(el, dict):
        return el
    else:
        raise ValueError('cannot get value of \'' + para + '\'')


def get_settings_file():
    """Return the file name of the default settings file.

    Returns
    -------
    string
    """
    return os.path.join(REPO_DIR, SETTINGS_FILE)


def print_settings():
    """Print the current settings."""
    print yaml.dump(read_settings(), default_flow_style=False)


def read_settings():
    """Return the current settings from the default settings file.

    Returns
    -------
    dict
    """
    filename = get_settings_file()
    # Read the settings file if it exist. Otherwise return an empty dictionary.
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            return yaml.load(f.read())
    else:
        return dict()


def update_settings(para, value):
    """Update the value of a configuration parameter. The para argument may
    contain a path expression. In this case all nested elements along the path
    are created if necessary.

    Raises ValueError if an invalid parameter name is given or if an existing
    text element is referenced as part of a path expression.

    Parameters
    ----------
    para: string
        Parameter path
    value: string
        New parameter value
    """
    config = read_settings()
    # Remove potential starting and traailing '/'
    if para.startswith('/'):
        para = para[1:]
    if para.endswith('/'):
        para = para[:-1]
    path = para.split('/')
    key = path[-1].strip()
    if key == '':
        raise ValueError('invalid parameter name \'' + para + '\'')
    # Find the element that is referenced by the path prefix. Create elements
    # along the path if necessary
    el = config
    for comp in path[:-1]:
        if not comp in el:
            el[comp] = dict()
        el = el[comp]
        if not isinstance(el, dict):
            raise ValueError('cannot create element under text value \'' + el + '\'')
    # Update the parameter value in the target element
    el[key] = value
    # Write modified configuration to disk
    write_settings(config)


def write_settings(config):
    """Write a configuration dictionary to the default settings file.

    Parameters
    ----------
    config: dict
        Configuration settings
    """
    filename = os.path.join(REPO_DIR, SETTINGS_FILE)
    with open(get_settings_file(), 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
