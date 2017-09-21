"""Experiment Reposirty
"""

import os
import sys

# ------------------------------------------------------------------------------
# Global Constants
# ------------------------------------------------------------------------------

"""Name of the directories that contains the reporitory data."""
COMMAND_DIR = 'commands'
REPO_DIR = '.exprepo'


"""Name of configuration files."""
BASE_FILE = 'BASE'
SETTINGS_FILE = 'SETTINGS'


"""Command names."""
# Create a clone of an existing repository
CMD_CLONE = 'clone'
CMD_CLONE_SOURCE = 'source'
# Registry of executable scripts
CMD_COMMAND = 'cmd'
CMD_COMMAND_ADD = 'add'
CMD_COMMAND_LIST = "list"
# Experiment configuration parameter
CMD_CONFIG = 'config'
CMD_CONFIG_SET = 'set'
CMD_CONFIG_SHOW = 'show'
# Initialize the experiment repository
CMD_INIT = 'init'
# Command history
CMD_HISTORY = 'history'
# Run a script as path of an experiment
CMD_RUN = 'run'


# ------------------------------------------------------------------------------
# Helper Methods
# ------------------------------------------------------------------------------

def get_base():
    """Get the path to the repository base directory. Not that the value in the
    BASE_FILE is a path expression that is relative to the working dorectory,
    not the REPO_DIR.

    Raises RuntimeError if the current directory does not contain a REPO_DIR.

    Returns
    -------
    string
    """
    filename = os.join(REPO_DIR, BASE_FILE)
    if not os.path.isfile(filename):
        raise RuntimeError('not a valid experiment repository')
    with open(filename, 'r') as f:
        return f.read().strip()
