#!/usr/bin/env python

import os
from doit.reporter import ConsoleReporter

PROJECT_DIR = os.path.dirname(os.path.join(os.path.dirname(__file__), '../'))
DATA_DIR    = os.path.join(PROJECT_DIR, 'data')
RESULTS_DIR = os.path.join(PROJECT_DIR, 'results')
FIGURES_DIR = os.path.join(PROJECT_DIR, 'figures')


class TermCodes:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def text(txt, code):
    return code + txt + TermCodes.ENDC


def get_console_size():
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
    except:
        rows, columns = 80, 80
    return int(rows), int(columns)


def major_divider(text=''):
    _, columns = get_console_size()
    if text:
        text = '== {0} '.format(text)
    return '\n{0}{1}'.format(text, '=' * (columns-len(text)))


def minor_divider(text=''):
    _, columns = get_console_size()
    if text:
        text = '-- {0} '.format(text)
    return '{0}{1}'.format(text, '-' * (columns-len(text)))


def title_with_actions(task):
    """return task name task actions"""
    if task.actions:
        title = "\n".join([str(action) for action in task.actions])
    # A task that contains no actions at all
    # is used as group task
    else:
        title = "Group: %s" % ", ".join(task.task_dep)
    return "Name: {name}\n{title}\n".format(
            name=text(task.name, TermCodes.HEADER),
            title=title)


class ColorReporter(ConsoleReporter):

    def execute_task(self, task):
        if task.actions and (task.name[0] != '_'):
            self.write(text(major_divider('RUN TASK'), TermCodes.WARNING))
            self.write('\n')
            self.write(task.title())
            self.write(text(minor_divider('task output'),
                       TermCodes.OKGREEN))
            self.write('\n')

    def skip_uptodate(self, task):
        if task.name[0] != '_':
            self.write(text(major_divider('TASK UP-TO-DATE'),
                            TermCodes.OKBLUE))
            self.write('\n')
            self.write(task.title())
    
    def skip_ignore(self, task):
        self.write(major_divider())
        super().skip_ignore(task)

    def _write_failure(self, result, write_exception=True):
        self.write(text(major_divider('TASK FAILURE'), TermCodes.FAIL))
        err = text(result['exception'].get_name(), TermCodes.FAIL)
        tsk = text(result['task'].name, TermCodes.HEADER)
        msg = '%s - taskid:%s\n' % (err, tsk)
        self.write(msg)
        if write_exception:
            self.write(result['exception'].get_msg())
            self.write("\n")


def flatten(L):
    return [item for sublist in L for item in sublist]


def replace_ext(filename, ext):
    return os.path.splitext(filename)[0] + ext


def replace_exts(files, ext):
    if type(files) is list:
        return [replace_ext(fn, ext) for fn in files]
    else:
        return {k:replace_ext(v, ext) for k,v in files.items()}


def isfile_filter(files):
    if type(files) is list:
        return [fn for fn in files if os.path.isfile(fn)]
    else:
        return {k:v for k,v in files.items() if os.path.isfile(v)}


