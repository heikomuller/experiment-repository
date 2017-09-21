"""Experiment Reposirty
"""

import sys

# ------------------------------------------------------------------------------
# Global Constants
# ------------------------------------------------------------------------------

"""Name of the directories that contains the reporitory data."""
COMMAND_DIR = 'commands'
REPO_DIR = '.exprepo'


"""Name of configuration files."""
HISTORY_FILE = 'HISTORY'
SETTINGS_FILE = 'SETTINGS'


"""Command names."""
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
CMD_INIT_SOURCE = 'source'
# Command history
CMD_HISTORY = 'history'
# Run a script as path of an experiment
CMD_RUN = 'run'
