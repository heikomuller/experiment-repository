#!/home/heiko/.venv/exp/bin/python

import sys

import exprepo as exp
from exprepo.command import add_command, list_commands, list_history, run_command
from exprepo.init import init_repository
from exprepo.settings import print_settings, update_settings


def help(prg_name):
    """Print the default help statement contaiing a listing and short
    description of the currently supported commands.

    Paramaters
    ----------
    prg_name : string
        Name with which the program was called
    """
    return """Usage: """ + prg_name + """ <command> [<arguments>]

These are the commands that are currently implements:

  init     Initialize a new experiment reposiroty
  config   Show and set the values of a configuration parameters
  add      Add a new command description to the repository
  run      Run a registered command
"""


def main(prg_name, args):
    """Main routine to execute a repository command.

    Parameters
    ----------
    prg_name : string
        Name with which the program was called
    args: list(string)
        List of command line arguments
    """
    # The first argument is the command name
    cmd_name = args[0]
    cmd_help = ['usage:', prg_name, args[0]]
    if cmd_name == exp.CMD_INIT:
        cmd_help += ['{', exp.CMD_INIT_SOURCE, '<source-dir>', '}']
        # Initialize a new repository. If no further arguments are given the
        # reposiroty is empty. If a source is specified the new repository is
        # initialized from the given source
        if len(args) == 1:
            init_repository()
        elif len(args) == 3 and args[1] == exp.CMD_INIT_SOURCE:
            try:
                init_repository(source_dir=args[2])
            except ValueError as ex:
                print prg_name + ' (ERROR): ' + str(ex)
        else:
            print ' '.join(cmd_help)
    elif cmd_name == exp.CMD_CONFIG:
        # Show and manipulate the experiment configuration. Expects at least one
        # addditional parameter specifying the sub-command
        cmd_help += [
            '[',
                exp.CMD_CONFIG_SHOW,
            '|',
                exp.CMD_CONFIG_SET, '<parameter>', '<value>',
            ']'
        ]
        if len(args) > 1:
            # Prints the current configuration if no arguments are given. To set
            # a configuration parameter provide two additional parameters: name of
            # the parameter and new value
            if len(args) == 2 and args[1] == exp.CMD_CONFIG_SHOW:
                print_settings()
            elif len(args) == 4 and args[1] == exp.CMD_CONFIG_SET:
                try:
                    update_settings(args[2], args[3])
                except ValueError as ex:
                    print prg_name + ' (ERROR): ' + str(ex)
            else:
                print ' '.join(cmd_help)
        else:
            print ' '.join(cmd_help)
    elif cmd_name == exp.CMD_COMMAND:
        # Show and manipulate the experiment script registry. Expects at least
        # one addditional parameter specifying the sub-command
        cmd_help += [
            '[',
                exp.CMD_COMMAND_LIST,
            '|',
                exp.CMD_COMMAND_ADD, '<name>', '<spec>',
            ']'
        ]
        if len(args) > 1:
            if len(args) == 2 and args[1] == exp.CMD_COMMAND_LIST:
                # Print a listing of the registered scripts
                list_commands()
            elif len(args) == 4 and args[1] == exp.CMD_COMMAND_ADD:
                try:
                    add_command(args[2], args[3])
                except ValueError as ex:
                    print prg_name + ' (ERROR): ' + str(ex)
            else:
                print ' '.join(cmd_help)
        else:
            print ' '.join(cmd_help)
    elif cmd_name == exp.CMD_HISTORY:
        # Print the list of experiment script commands that have been run
        list_history()
    elif cmd_name == exp.CMD_RUN:
        # Run a registered experiment command. Expects the script name as an
        # additional argument
        cmd_help += ['<name>']
        if len(args) == 2:
            try:
                run_command(prg_name, args[1])
            except ValueError as ex:
                print prg_name + ' (ERROR): ' + str(ex)
        else:
            print ' '.join(cmd_help)
    elif cmd_name == '--help':
        print help(prg_name)
    else:
        print prg_name + ': \'' + cmd_name + '\' is not a ' + prg_name + ' command. See \'' + prg_name + ' --help.'


if __name__ == '__main__':
    # Extract the program name as the last component of the command path
    prg_name = sys.argv[0].split('/')[-1]
    if len(sys.argv) < 2:
        print help(prg_name)
        sys.exit(-1)
    else:
        main(prg_name, sys.argv[1:])
