"""Experiment Reposirty
"""

import os
import sys

# ------------------------------------------------------------------------------
# Global Constants
# ------------------------------------------------------------------------------

"""Name of the directories that contains the reporitory data."""
COMMAND_DIR = 'commands'
REPO_DIR = '.xpr'


"""Name of configuration files."""
BASE_FILE = 'BASE'
LOG_FILE = 'LOG'
SETTINGS_FILE = 'SETTINGS'


"""Command names."""
# Create a clone of an existing repository
CMD_CLONE = 'clone'
CMD_CLONE_SOURCE = 'source'
# Registry of executable scripts
CMD_COMMAND = 'command'
CMD_COMMAND_ADD = 'add'
CMD_COMMAND_LIST = "list"
CMD_COMMAND_UPDATE = "update"
# Experiment configuration parameter
CMD_CONFIG = 'config'
CMD_CONFIG_SET = 'set'
CMD_CONFIG_SHOW = 'show'
# Initialize the experiment repository
CMD_INIT = 'init'
# Command history
CMD_LOG = 'log'
# Run a script as part of an experiment
CMD_RUN = 'run'
# Submit a script without running it locally
CMD_SUBMIT = 'submit'


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
    filename = os.path.join(REPO_DIR, BASE_FILE)
    if not os.path.isfile(filename):
        raise RuntimeError('not a valid experiment repository')
    with open(filename, 'r') as f:
        return f.read().strip()
