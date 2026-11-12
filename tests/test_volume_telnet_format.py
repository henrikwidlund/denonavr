#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the telnet wire format of async_set_volume."""

import logging

import pytest

from denonavr.foundation import DenonAVRDeviceInfo
from denonavr.volume import DenonAVRVolume, convert_telnet_volume
from tests.test_helpers import DeviceTestFixture

# pylint: disable=protected-access


@pytest.mark.parametrize(
    "volume,expected",
    [
        (-80, "00"),
        (-75.5, "045"),
        (-75, "05"),
        (-36.5, "435"),
        (-35.5, "445"),
        (-35, "45"),
        (0, "80"),
        (17.5, "975"),
        (18, "98"),
    ],
)
def test_convert_telnet_volume(volume, expected):
    """Test that a half step adds a digit 5 to the two digit whole part."""
    assert convert_telnet_volume(volume) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "volume,expected",
    [(-80, "MV00"), (-75.5, "MV045"), (-35.5, "MV445"), (-35, "MV45"), (18, "MV98")],
)
async def test_async_set_volume_sends_half_step(volume, expected):
    """Test that the command keeps the half dB of the requested volume."""
    fixture = DeviceTestFixture(True)
    device = DenonAVRVolume(device=fixture.device_info)
    device._max_volume_callback("Main", "SS", "VCTZMALIM 98")
    device._volume_callback("Main", "", "50")
    await fixture.async_execute(device.async_set_volume(volume))
    fixture._mock_telnet.assert_called_once()
    assert fixture._mock_telnet.call_args[0][0] == expected


@pytest.mark.asyncio
async def test_async_set_volume_clamps_to_max_volume():
    """Test that a volume above the custom max is sent as the max."""
    fixture = DeviceTestFixture(True)
    device = DenonAVRVolume(device=fixture.device_info)
    device._max_volume_callback("Main", "", "VCTZMALIM 30")
    device._volume_callback("Main", "", "50")
    await fixture.async_execute(device.async_set_volume(18))
    fixture._mock_telnet.assert_called_once()
    assert fixture._mock_telnet.call_args[0][0] == "MV30"


@pytest.mark.parametrize(
    "volume,expected", [(-80, "00"), (-54.5, "26"), (-55.5, "25"), (-55, "25")]
)
def test_convert_telnet_volume_without_half_step(volume, expected):
    """Test that the volume is rounded to a whole dB."""
    assert convert_telnet_volume(volume, half_step=False) == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "zone,volume,expected",
    [
        ("Zone2", -54.5, "Z226"),
        ("Zone2", -55, "Z225"),
        ("Zone3", 10.5, "Z391"),
        ("Zone3", 10, "Z390"),
    ],
)
async def test_async_set_volume_zone_sends_whole_db(zone, volume, expected, caplog):
    """Test that zone 2 and 3 never send a half step and warn about a half dB."""
    fixture = DeviceTestFixture(True)
    fixture.device_info = DenonAVRDeviceInfo(
        api=fixture.api, telnet_api=fixture.telnet_api, zone=zone
    )
    device = DenonAVRVolume(device=fixture.device_info)
    with caplog.at_level(logging.WARNING):
        await fixture.async_execute(device.async_set_volume(volume))
    fixture._mock_telnet.assert_called_once()
    assert fixture._mock_telnet.call_args[0][0] == expected
    assert ("does not accept half steps" in caplog.text) == (volume % 1 != 0)


@pytest.mark.asyncio
async def test_async_set_volume_main_zone_half_step_no_warning(caplog):
    """Test that the main zone sends a half step without a warning."""
    fixture = DeviceTestFixture(True)
    device = DenonAVRVolume(device=fixture.device_info)
    device._volume_callback("Main", "", "50")
    with caplog.at_level(logging.WARNING):
        await fixture.async_execute(device.async_set_volume(-35.5))
    assert fixture._mock_telnet.call_args[0][0] == "MV445"
    assert "half steps" not in caplog.text
