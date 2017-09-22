"""Everythin for command registry."""


import exprepo as exp
import os
from settings import get_settings
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

def add_command(name, spec, replace=False):
    """Create or replace a script command in the experiment's command registry.

    Raises ValueError if (create) a command with the given name already exists,
    or (replace) no command with the given name exists.

    Parameters
    ----------
    name: string
        Command name
    spec: string
        Command specification as a command line string with configuration
        parameters enclosed in << >>
    replace: bool, optional
        Flag indicating whether a new command is added to the registry or an
        existing one is replaced.
    """
    # Get file for the new command. Raise an expeption if (1) the file already
    # exists and the replace flag is set to False, or (2) the file does not
    # exist and the replace flag is True
    filename = os.path.join(
        get_commands_dir(),
        name.lower() + COMMAND_SPEC_SUFFIX
    )
    if not replace and os.path.isfile(filename):
        raise ValueError('command \'' + name + '\' already exists')
    elif replace and not os.path.isfile(filename):
        raise ValueError('command \'' + name + '\' does not exist')
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

    Raises RuntimeError if the directory does not exist.

    Returns
    -------
    string
    """
    command_dir = os.path.join(exp.get_base(), exp.REPO_DIR, exp.COMMAND_DIR)
    if not os.path.isdir(command_dir):
        raise RuntimeError('not a valid experiment repository')
    return command_dir


def get_log_file():
    """Get name of the repository file that stores the command execution log.

    Returns
    -------
    string
    """
    return os.path.join(exp.REPO_DIR, exp.LOG_FILE)


def list_commands():
    """List the names and specifications of all scripts that are currently
    registerd.
    """
    commands = get_commands()
    # Print commands sorted by their name
    for cmd_name in sorted(commands.keys()):
        print cmd_name


def print_log():
    """Print the log of experiment commands to standard output."""
    filename = get_log_file()
    # The file may not exist if no command has been executed yet
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            for line in f:
                print line.strip()


def run_command(prg_name, name, args, run_local=True):
    """Run the experiment script with the given name. Constructs the command
    to run the script from the current configuration settings and optional
    arguments that overwrite these settings. The script is only execute if the
    run local flag is True.

    Raises ValueError if the specified command is unknown or if the provided
    arguments are of invalid format.

    Parameters
    ----------
    name: string
        Name of the script that is being run_command
    args: list(string)
        Arguments that override the current configurations ettings (expected
        format is <key>=<value>)
    run_local: bool, optional
        Flag indicating whether to actuall execute the script or only print
        and log the command line command for submission on a remote machine.
    """
    commands = get_commands()
    if not name in commands:
        raise ValueError('unknown command \'' + name + '\'')
    # Get a dictionary of arguments that override the configuration settings
    local_args = dict()
    for arg in args:
        pos = arg.find('=')
        if pos < 0:
            raise ValueError('invalid argument \'' + arg + '\'')
        local_args[arg[:pos]] = arg[pos+1:]
    # Read the current experiment configuration settings
    config = get_settings()
    # Create the list of command components
    cmd = []
    for obj in commands[name]:
        if obj.is_var:
            if obj.value in local_args:
                val = local_args[obj.value]
            else:
                val = config.get_value(obj.value)
            cmd.append(val)
        else:
            cmd.append(obj.value)
    # Run the command if run local flag is True
    if run_local:
        print prg_name + ' (RUN): ' + ' '.join(cmd)
        result = subprocess.call(cmd)
        # Add command to log if successfule (i.e., result is 0)
        if result == 0:
            with open(get_log_file(), 'a') as f:
                f.write(' '.join(cmd) + '\n')
    else:
        print prg_name + ' (SUBMIT): ' + ' '.join(cmd)
        with open(get_log_file(), 'a') as f:
            f.write('*' + ' '.join(cmd) + '\n')


def show_command(name):
    """Print specification for the registered command with the given name.

    Raises ValueError if no command with the given name is found.

    Parameters
    ----------
    name: string
        Name of the command to be printed
    """
    commands = get_commands()
    if name in commands:
        print 'command: ' + name + '\n'
        print 'parameters:'
        i = 1
        for obj in commands[name]:
            print '(' + str(i) + ')  ' + obj.to_spec
            i += 1
    else:
        raise ValueError('unknown command \'' + name + '\'')
