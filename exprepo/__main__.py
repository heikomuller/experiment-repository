#!/home/heiko/.venv/exp/bin/python

import sys

import exprepo as exp
import exprepo.command as cmd
from exprepo.init import clone_repository, init_repository
from exprepo.settings import print_settings, update_settings
from exprepo.settings import print_global_variables, update_global_variables


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
  clone    Create a local copy of the experiment repository
  command  Manage scripts that are run as part of the experiment
  config   Show and set the values of a configuration parameters
  env   Show and set the global variables
  log      Show execution history of script commands
  run      Run a registered script command
  submit   Submit a script to run on a remote machine
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
        # Initialize a new repository. Init does not take any further arguments.
        if len(args) == 1:
            init_repository()
        else:
            print ' '.join(cmd_help)
    elif cmd_name == exp.CMD_CLONE:
        # Create a clone repository in the current working directory. Clone
        # takes and optional source argument that specifies the directory from
        # which settings are copied.
        cmd_help += ['{', exp.CMD_CLONE_SOURCE, '<source-dir>', '}']
        if len(args) == 1:
            clone_repository()
        elif len(args) == 3 and args[1] == exp.CMD_CLONE_SOURCE:
            clone_repository(source_dir=args[2])
        else:
            print ' '.join(cmd_help)
    elif cmd_name == exp.CMD_CONFIG:
        # Show and manipulate the experiment configuration. Expects at least one
        # addditional parameter specifying the sub-command: Print (SHOW) or
        # manipulate (SET). To delete a configuration parameter omit the value
        # in a SET statement
        cmd_help += [
            '[',
                exp.CMD_CONFIG_SHOW,
            '|',
                exp.CMD_CONFIG_SET, '<parameter>', '{<value>}',
            ']'
        ]
        if len(args) > 1:
            #
            if len(args) == 2 and args[1] == exp.CMD_CONFIG_SHOW:
                print_settings()
            elif len(args) == 3 and args[1] == exp.CMD_CONFIG_SET:
                update_settings(args[2])
            elif len(args) == 4 and args[1] == exp.CMD_CONFIG_SET:
                update_settings(args[2], args[3])
            else:
                print ' '.join(cmd_help)
        else:
            print ' '.join(cmd_help)
    elif cmd_name == exp.CMD_GLOBAL:
        # Show and manipulate global variables that descript the local
        # environment. Expects at least one addditional parameter specifying the
        # sub-command: Print (SHOW) or manipulate (SET). To delete a variable
        # omit the value in a SET statement
        cmd_help += [
            '[',
                exp.CMD_GLOBAL_SHOW,
            '|',
                exp.CMD_GLOBAL_SET, '<variable>', '{<value>}',
            ']'
        ]
        if len(args) > 1:
            if len(args) == 2 and args[1] == exp.CMD_GLOBAL_SHOW:
                print_global_variables()
            elif len(args) == 3 and args[1] == exp.CMD_GLOBAL_SET:
                update_global_variables(args[2])
            elif len(args) == 4 and args[1] == exp.CMD_GLOBAL_SET:
                update_global_variables(args[2], args[3])
            else:
                print ' '.join(cmd_help)
        else:
            print ' '.join(cmd_help)
    elif cmd_name == exp.CMD_COMMAND:
        # Show and manipulate the experiment script registry. Expects at least
        # one addditional parameter specifying the sub-command
        cmd_help += [
            '[',
                exp.CMD_COMMAND_LIST, '{<name>}'
            '|',
                exp.CMD_COMMAND_ADD, '<name>', '<spec>',
            '|',
                exp.CMD_COMMAND_UPDATE, '<name>', '<spec>',
            ']'
        ]
        if len(args) > 1:
            if len(args) == 2 and args[1] == exp.CMD_COMMAND_LIST:
                # Print a listing of the registered scripts
                cmd.list_commands()
            elif len(args) == 3 and args[1] == exp.CMD_COMMAND_LIST:
                # Print a listing of the registered scripts
                cmd.show_command(args[2])
            elif len(args) == 4 and args[1] == exp.CMD_COMMAND_ADD:
                # Add a new command to the script registry
                cmd.add_command(args[2], args[3])
            elif len(args) == 4 and args[1] == exp.CMD_COMMAND_UPDATE:
                # Update the specification of an existing command
                cmd.add_command(args[2], args[3], replace=True)
            else:
                print ' '.join(cmd_help)
        else:
            print ' '.join(cmd_help)
    elif cmd_name == exp.CMD_LOG:
        # Print the list of experiment script commands that have been run
        cmd.print_log()
    elif cmd_name == exp.CMD_RUN:
        # Run a registered experiment command. Expects the script name as an
        # additional argument and an optional list of command arguments.
        cmd_help += ['<name>', '{<arguments>}']
        if len(args) >= 2:
            cmd.run_command(prg_name, args[1], args[2:])
        else:
            print ' '.join(cmd_help)
    elif cmd_name == exp.CMD_SUBMIT:
        # Submit a registered experiment command for execution on a remote host.
        # Expects the script name as an additional argument and an optional list
        # of command arguments.
        cmd_help += ['<name>', '{<arguments>}']
        if len(args) >= 2:
            cmd.run_command(prg_name, args[1], args[2:], run_local=False)
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
        try:
            main(prg_name, sys.argv[1:])
        except (ValueError, RuntimeError) as ex:
            print prg_name + ' (ERROR): ' + str(ex)
