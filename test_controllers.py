"""
Development and debugging tool.

This file should be run with the interactive option. For example,

    $ python3 -i test_controllers.py bapa/modules/officers/controllers.py

will provide a shell with a module named `c` exposing all of the endpoints in
controllers.py
"""

import sys
import importlib
from bapa import db
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    if file_path.endswith('.py'):
        file_path = file_path[:-3]
    module_path = '.'.join(file_path.split('/'))
    c = importlib.import_module(module_path)
