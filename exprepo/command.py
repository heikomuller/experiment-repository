"""Everythin for command registry."""


import exprepo as exp
import os
from settings import get_setting, read_settings
import subprocess
import yaml


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

"""Suffix for files containing command specification."""
COMMAND_SPEC_SUFFIX = '.cmd'

"""Type of components in a command specification."""
COMMAND_ELEMENT_CONST = 'const'
COMMAND_ELEMENT_VAR = 'var'
COMMAND_ELEMENT_TYPES = [COMMAND_ELEMENT_CONST, COMMAND_ELEMENT_VAR]


# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------

class CmdElement(object):
    def __init__(self, element_type, value):
        if not element_type in COMMAND_ELEMENT_TYPES:
            raise ValueError('invalid element type \'' + element_type + '\'')
        self.element_type = element_type
        self.value = value

    @staticmethod
    def from_dict(obj):
        if obj['type'] == COMMAND_ELEMENT_CONST:
            return ConstantCmdElement(obj['value'])
        elif obj['type'] == COMMAND_ELEMENT_VAR:
            return VariableCmdElement(obj['value'])
        else:
            raise RuntimeError('unexpected element type: ' + str(obj['type']))

    @property
    def is_const(self):
        return self.element_type == COMMAND_ELEMENT_CONST

    @property
    def is_var(self):
        return self.element_type == COMMAND_ELEMENT_VAR

    def to_dict(self):
        return {'type' : self.element_type, 'value': self.value}


class ConstantCmdElement(CmdElement):
    def __init__(self, value):
        super(ConstantCmdElement, self).__init__(COMMAND_ELEMENT_CONST, value)

    @property
    def to_spec(self):
        return self.value


class VariableCmdElement(CmdElement):
    def __init__(self, value):
        super(VariableCmdElement, self).__init__(COMMAND_ELEMENT_VAR, value)

    @property
    def to_spec(self):
        return '<<' + self.value + '>>'


# ------------------------------------------------------------------------------
# API Methods
# ------------------------------------------------------------------------------

def add_command(name, spec):
    """
    """
    # Get file for the new command. If the file already exists, a command with
    # the givenname has been registered before and we raise a ValueError.
    filename = os.path.join(
        get_commands_dir(),
        name.lower() + COMMAND_SPEC_SUFFIX
    )
    if os.path.isfile(filename):
        raise ValueError('command \'' + name + '\' already exists')
    # Parse the command specification
    cmd = []
    for token in spec.split():
        if token.startswith('<<') and token.endswith('>>'):
            cmd.append(VariableCmdElement(token[2:-2]).to_dict())
        else:
            cmd.append(ConstantCmdElement(token).to_dict())
    # Write command specification to file (currently in Yaml format)
    with open(filename, 'w') as f:
        yaml.dump(cmd, f, default_flow_style=False)


def get_commands():
    """Get a dictionary containing the command specifications for the commands
    that are currently registered. The dictionary key is the command name.

    Returns
    -------
    dict
    """
    # Collect command specifications in a dictionary
    commands = dict()
    reg_dir = get_commands_dir()
    for f_name in os.listdir(reg_dir):
        if f_name.endswith(COMMAND_SPEC_SUFFIX):
            # Read command specification and add to list of commands
            cmd_name = f_name[:-len(COMMAND_SPEC_SUFFIX)].lower()
            with open(os.path.join(reg_dir, f_name), 'r') as f:
                commands[cmd_name] = [
                    CmdElement.from_dict(obj) for obj in yaml.load(f.read())
                ]
    return commands


def get_commands_dir():
    """Return the name of the directory where the command registry is
    maintained.

    Returns
    -------
    string
    """
    return os.path.join(exp.REPO_DIR, exp.COMMAND_DIR)


def get_history_file():
    """Get name of the repository file that stores the command execution
    history.

    Returns
    -------
    string
    """
    return os.path.join(exp.REPO_DIR, exp.HISTORY_FILE)


def list_commands():
    """List the names and specifications of all scripts that are currently
    registerd.
    """
    commands = get_commands()
    # Print commands sorted by their name
    for cmd_name in sorted(commands.keys()):
        print cmd_name
        command_spec = []
        for obj in commands[cmd_name]:
            command_spec.append(obj.to_spec)
        print '  ' + ' '.join(command_spec)


def list_history():
    """Print the history of experiment commands to standard output."""
    filename = get_history_file()
    # The file may not exist if no command has been executed yet
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            for line in f:
                print line.strip()


def run_command(prg_name, name):
    """Run the experiment script with the given name.

    Raises ValueError if the specified command is unknown.

    Parameters
    ----------
    name: string
        Name of the script that is being run_command
    """
    commands = get_commands()
    if not name in commands:
        raise ValueError('unknown command \'' + name + '\'')
    # Read the current experiment configuration settings
    config = read_settings()
    # Create the list of command components
    cmd = []
    for obj in commands[name]:
        if obj.is_var:
            cmd.append(get_setting(config, obj.value))
        else:
            cmd.append(obj.value)
    # Run the command
    print prg_name + ' (RUN): ' + ' '.join(cmd)
    result = subprocess.call(cmd)
    # Add command to history if successfule (i.e., result is 0)
    if result == 0:
        with open(get_history_file(), 'a') as f:
            f.write(' '.join(cmd) + '\n')
