#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains helper functions for tests.

:copyright: (c) 2016 by Oliver Goetz.
:license: MIT, see LICENSE for more details.
"""

from unittest.mock import PropertyMock, patch


def patch_telnet_available(device_info):
    """Patch telnet_available property to return True."""
    return patch.object(
        type(device_info),
        "telnet_available",
        new_callable=PropertyMock,
        return_value=True,
    )
