#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pytest configuration for denonavr tests.

:copyright: (c) 2016 by Oliver Goetz.
:license: MIT, see LICENSE for more details.
"""

import sys
from pathlib import Path

# Ensure the denonavr package is importable
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

