#!/usr/bin/env doit

import os
import sys
# ugly snippet to maintain a sane project dir structure
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from doit.task import clean_targets
import json

from project.utils import (ColorReporter, title_with_actions,
                           replace_ext)

DOIT_CONFIG  = {'verbosity': 2,
                'reporter': ColorReporter}

metadata = json.load(open('data.json'))
for name, filename in metadata.items():
    metadata[name] = json.load(open(filename))


def download_sra(acc, folder):
    cmd = 'get-run.py -d {0} -F "{{acc}}.sra" -a -i "{1}"'.format(folder,
                                                                acc)
    return cmd, os.path.join(folder, '{0}.sra'.format(acc))


def fastq_dump(input_filename):
    base = os.path.splitext(input_filename)[0]
    output = base + '.pe.fastq.gz'
    cmd = 'fastq-dump {0} --split-spot -I --skip-technical'\
          ' --read-filter pass --gzip -Z > {1}'.format(input_filename,
                                                       output)

    return cmd, output


def task_create_mmetsp_folders():

    def write_meta(folder, data):
        with open(os.path.join(folder, 'meta.json'), 'w') as fp:
            json.dump(data, fp, indent=4)

    for name, accs in metadata['MMETSP'].items():
        folder = os.path.join('MMETSP', name)
        mkdir = 'mkdir -p {0}'.format(folder)
        
        yield {'name': 'create_folder_{0}'.format(name),
               'title': title_with_actions,
               'targets': [os.path.join(folder, 'meta.json')],
               'file_dep': ['mmetsp_subset.json'],
               'actions': [mkdir,
                           (write_meta, [folder, accs])],
               'clean': True}


def task_download_mmetsp():
    for name, accs in metadata['MMETSP'].items():
        for acc, data in accs.items():
            folder = os.path.join('MMETSP', name)
            dl_cmd, sra_filename = download_sra(acc, folder)
        
            yield {'name': 'download_sra_{0}'.format(acc),
                   'title': title_with_actions,
                   'file_dep': [os.path.join(folder, 'meta.json')],
                   'targets': [sra_filename],
                   'actions': [dl_cmd],
                   'clean': True}


def task_unpack_mmetsp():
    for name, accs in metadata['MMETSP'].items():
        for acc, data in accs.items():
            folder = os.path.join('MMETSP', name)
            _, sra_filename = download_sra(acc, folder)
            unpack, fastq_filename = fastq_dump(sra_filename)

            yield {'name': 'unpack_sra_{0}'.format(acc),
                   'title': title_with_actions,
                   'file_dep': [sra_filename],
                   'targets': [fastq_filename],
                   'actions': [unpack],
                   'clean': True}
