# -*- coding: utf-8 -*-
import subprocess
import re
import sys

MAX_LINE_LENGTH = 20


def log(log_type, string=None):
    if log_type == 'title':
        sys.stdout.write(string)
        for i in range(0, MAX_LINE_LENGTH - len(string)):
            sys.stdout.write(' ')
        sys.stdout.flush()
    elif log_type == 'ok':
        print('     [\033[00;32m OK \033[0m]')
    elif log_type == 'skip':
        print('   [\033[00;31m SKIP \033[0m]')
    elif log_type == 'failure':
        print('[\033[00;31m FAILURE \033[0m]')
        print(string)


def _normalize_boolean(value):
    """Convert a string into a Boolean value.

    :param value: the string to be converted
    """
    return value.lower() == 'true'


def _find_files(options, regex):
    paths = options['directory'].split('\n')
    cmd = ['find', '-L'] + paths + ['-regex', regex]
    process_files = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=subprocess.PIPE
    )
    files, err = process_files.communicate()
    return files


def _read_subprocess_output(cmd, output_file):
    """Run cmd and read the output from output_file.

    :param cmd: list containing command and options.
    :param output_file: file that will store the command output.
    :return: command output read from output_file.
    """
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.STDOUT,
        stdout=output_file
    )
    process.wait()
    output_file.flush()
    output_file.seek(0)
    output = output_file.read()
    return output, process.returncode


def _process_output(output, old, new):
    """Replace all occurrences of substring 'old' with 'new' in 'output'.

    :param output: string containing command output
    :param old: substring to be found
    :param new: replace substring
    :return: string containing processed command output
    """
    error = re.compile(old)
    output = map(lambda x: error.sub(new, x), output.splitlines())
    return u'\n'.join(output)
