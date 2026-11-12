#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests that the raw sound modes AUTO and STANDARD are matched."""

import logging

import pytest

from denonavr.soundmode import DenonAVRSoundMode
from tests.test_helpers import DeviceTestFixture

# pylint: disable=protected-access


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("AUTO", "AUTO"),
        ("Auto", "AUTO"),
        ("STANDARD", "STANDARD"),
        ("Standard", "STANDARD"),
    ],
)
def test_match_sound_mode_auto_and_standard(raw, expected, caplog):
    """Test that the raw mode is matched without a warning."""
    device = DenonAVRSoundMode(device=DeviceTestFixture(True).device_info)
    device._sound_mode_raw = raw
    with caplog.at_level(logging.WARNING):
        assert device.match_sound_mode() == expected
    assert "Not able to match" not in caplog.text
