#!/usr/bin/env doit

import os
import sys
# ugly snippet to maintain a sane project dir structure
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from doit.task import clean_targets
import json

from project.utils import (ColorReporter, title_with_actions,
                           replace_ext, DATA_DIR, RESULTS_DIR)

DOIT_CONFIG  = {'verbosity': 2,
                'reporter': ColorReporter}

metadata = json.load(open(os.path.join(DATA_DIR, 'data.json')))
for name, filename in metadata.items():
    metadata[name] = json.load(open(filename))


