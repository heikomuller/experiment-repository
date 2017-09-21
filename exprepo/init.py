"""Everything needed to initialize the repository."""

from exprepo import BASE_FILE, COMMAND_DIR, REPO_DIR, SETTINGS_FILE
from exprepo.command import COMMAND_SPEC_SUFFIX
import json
import os
from shutil import copyfile


def create_repository():
    """Creating the repository directory in the current working directory.

    Raises RuntimeError if a repository directory already exists in the current
    working directory.
    """
    if os.path.isfile(REPO_DIR) or os.path.isdir(REPO_DIR):
        raise RuntimeError('existing repository detected')
    os.mkdir(REPO_DIR)


def init_repository():
    """Initialize an experiment repository by creating the required folders
    and files.

    Raises RuntimeError if a repository directory already exists in the current
    working directory.
    """
    create_repository()
    os.mkdir(os.path.join(REPO_DIR, COMMAND_DIR))
    with open(os.path.join(REPO_DIR, BASE_FILE), 'w') as f:
        f.write('.')


def clone_repository(source_dir=None):
    """Initialize a cloned experiment repository by creating the required folder
    and setting file. Allows to specify an existing repository as source from
    which the current settings are copied as iitial values for the new
    repository.

    Raises ValueError if a specified source directory does not exist or is not
    an experiment repository directory.

    Raises RuntimeError if no base repository is found in the upward path of
    this current working directory or if a repository directory already exists
    in the current working directory.

    Parameters
    ----------
    source_dir: string, optional
        Directory containing an experiment repository from which settings will
        be copied.
    """
    # Raise an exception if a repository directory already exists in the current
    # working directory
    if os.path.isfile(REPO_DIR) or os.path.isdir(REPO_DIR):
        raise RuntimeError('existing repository detected')
    # Find base directory
    base_path = '.'
    found = False
    while os.path.isdir(base_path):
        base_path = os.path.join(base_path, '..')
        if os.path.isdir(os.path.join(base_path, REPO_DIR)):
            if os.path.isdir(os.path.join(base_path, REPO_DIR, COMMAND_DIR)):
                found = True
                break
    if not found:
        raise RuntimeError('no base repository found')
    # Set the default settings file if a source directory is specified
    settings_file = None
    if not source_dir is None:
        if not os.path.isdir(source_dir):
            raise ValueError('unknown directory \'' + source_dir + '\'')
        repo_dir = os.path.join(source_dir, REPO_DIR)
        if not os.path.isdir(repo_dir):
            raise ValueError('not a valid repository \'' + source_dir + '\'')
        settings_file = os.path.join(repo_dir, SETTINGS_FILE)
    # Create the repository directory and write base path to BASE file
    create_repository()
    with open(os.path.join(REPO_DIR, BASE_FILE), 'w') as f:
        f.write(base_path)
    # Copy default settings file if it exists
    if not settings_file is None:
        if os.path.isfile(settings_file):
            copyfile(settings_file, os.path.join(REPO_DIR, SETTINGS_FILE))
