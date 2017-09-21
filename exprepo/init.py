"""Everything needed to initialize the repository."""

from exprepo import BASE_FILE, COMMAND_DIR, REPO_DIR, SETTINGS_FILE
from exprepo.command import COMMAND_SPEC_SUFFIX
import json
import os
from shutil import copyfile


def init_repository():
    """Initialize an experiment repository by creating the required folders
    and files.
    """
    os.mkdir(REPO_DIR)
    os.mkdir(os.path.join(REPO_DIR, COMMAND_DIR))
    with open(os.path.join(REPO_DIR, BASE_FILE), 'w') as f:
        f.write('./')


def clone_repository(source_dir=None):
    """Initialize an experiment repository by creating the required folders
    and files.
    Allows to specify an existing repository as source from which the settings
    and registered commands will be copied.

    Raises ValueError if a specified source directory does not exist or is not
    an experiment repository directory.

    Parameters
    ----------
    source_dir: string, optional
        Directory containing an experiment repository from which settings and
        registered commands will be copied.
    """
    if not source_dir is None:
        if not os.path.isdir(source_dir):
            raise ValueError('unknown directory \'' + source_dir + '\'')
        repo_dir = os.path.join(source_dir, REPO_DIR)
        if not os.path.isdir(repo_dir):
            raise ValueError('not a valid repository \'' + source_dir + '\'')
        command_dir = os.path.join(repo_dir, COMMAND_DIR)
        if not os.path.isdir(command_dir):
            raise ValueError('not a valid repository \'' + source_dir + '\'')
        # Create directory structure and copy existing files
        create_directories()
        # Copy settings from existing repository (if it exists)
        settings_file = os.path.join(repo_dir, SETTINGS_FILE)
        if os.path.isfile(settings_file):
            copyfile(settings_file, os.path.join(REPO_DIR, SETTINGS_FILE))
        # Copy commands from exosting repository
        command_target = os.path.join(REPO_DIR, COMMAND_DIR)
        for f_name in os.listdir(command_dir):
            if f_name.endswith(COMMAND_SPEC_SUFFIX):
                copyfile(
                    os.path.join(command_dir, f_name),
                    os.path.join(command_target, f_name)
                )
    else:
        create_directories()
