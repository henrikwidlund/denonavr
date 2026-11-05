#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for the advanced audio and video info of DenonAVRDeviceInfo."""

import asyncio
from unittest.mock import AsyncMock, PropertyMock, patch

import pytest

from denonavr.foundation import channel_status_to_str
from tests.test_helpers import DeviceTestFixture

# pylint: disable=protected-access


def _device():
    return DeviceTestFixture(True).device_info


@pytest.mark.parametrize(
    "callback, event, parameter, attribute, expected",
    [
        (
            "_ss_callback",
            "SS",
            "INFSIGRES I 4K60",
            "video_hdmi_signal_in",
            "4K60",
        ),
        (
            "_ss_callback",
            "SS",
            "INFSIGRES O 1080p",
            "video_hdmi_signal_out",
            "1080p",
        ),
        (
            "_ss_callback",
            "SS",
            "INFSIGRES I ---",
            "video_hdmi_signal_in",
            None,
        ),
        ("_sy_callback", "SY", "SDVIN 4K24", "video_hdmi_signal_in", "4K24"),
        (
            "_sy_callback",
            "SY",
            "SDVOUT 4K24",
            "video_hdmi_signal_out",
            "4K24",
        ),
        (
            "_ss_callback",
            "SS",
            "INFAISFSV 441",
            "audio_sampling_rate",
            "44.1",
        ),
        (
            "_ss_callback",
            "SS",
            "INFAISFSV 48K",
            "audio_sampling_rate",
            "48",
        ),
        (
            "_ss_callback",
            "SS",
            "INFAISFSV NON",
            "audio_sampling_rate",
            None,
        ),
        ("_ss_callback", "SS", "INFSIGHDR I HDR10", "hdr_input", "HDR10"),
        ("_ss_callback", "SS", "INFSIGHDR O ---", "hdr_output", None),
        ("_ss_callback", "SS", "INFSIGPIX 12", "pixel_depth_input", "8-bit"),
        ("_ss_callback", "SS", "INFSIGPIX 12", "pixel_depth_output", "10-bit"),
        ("_ss_callback", "SS", "INFSIGPIX 01", "pixel_depth_input", "Unknown"),
        ("_ss_callback", "SS", "INFSIGPIX 01", "pixel_depth_output", "8-bit"),
        ("_ss_callback", "SS", "INFSIGPIX 33", "pixel_depth_input", "12-bit"),
        ("_ss_callback", "SS", "INFSIGFRL I 48G", "max_frl_input", "48G"),
        ("_ss_callback", "SS", "INFSIGFRL O ---", "max_frl_output", None),
        ("_ss_callback", "SS", "INFSIGFRL I48G", "max_frl_input", "48G"),
        ("_ss_callback", "SS", "INFSIGFRL I---", "max_frl_input", None),
        ("_ss_callback", "SS", "INFSIGFRL O---", "max_frl_output", None),
        ("_ss_callback", "SS", "INFSIGCOS 23", "colorspace_input", "4:4:4"),
        ("_ss_callback", "SS", "INFSIGCOS 23", "colorspace_output", "RGB"),
        ("_ss_callback", "SS", "INFSIGCOS 88", "colorspace_input", "4:2:0"),
        ("_ss_callback", "SS", "INFSIGCOS 11", "colorspace_output", "4:2:2"),
        ("_ss_callback", "SS", "INFSIGCOS 03", "colorspace_input", None),
        ("_ss_callback", "SS", "INFSIGCOS 03", "colorspace_output", "RGB"),
        (
            "_ss_callback",
            "SS",
            "INFSIGCOS 99",
            "colorspace_input",
            "4:2:2/BT.2020",
        ),
        (
            "_sy_callback",
            "SY",
            "HDMIDIAGMAXRES 4K18G",
            "max_resolution",
            "4K18Gbps",
        ),
        (
            "_sy_callback",
            "SY",
            "HDMIDIAGMAXRES NO",
            "max_resolution",
            "No limit",
        ),
        (
            "_sy_callback",
            "SY",
            "SDA Dolby Atmos",
            "audio_signal",
            "Dolby Atmos",
        ),
        ("_sy_callback", "SY", "SDA Unknown", "audio_signal", "-"),
        (
            "_sy_callback",
            "SY",
            "SMI Dolby Atmos",
            "audio_sound",
            "Dolby Atmos",
        ),
        (
            "_op_callback",
            "OP",
            "INFINS " + "22000000".ljust(32, "0"),
            "input_channels",
            "2.0",
        ),
        (
            "_op_callback",
            "OP",
            "INFASP " + "22222222".ljust(32, "0"),
            "output_channels",
            "7.1",
        ),
    ],
)
def test_callbacks(callback, event, parameter, attribute, expected):
    """Test that telnet events update the properties."""
    device = _device()
    assert getattr(device, attribute) is None
    getattr(device, callback)("Main", event, parameter)
    assert getattr(device, attribute) == expected


@pytest.mark.parametrize(
    "colorspace, hdr, expected",
    [
        ("INFSIGCOS 22", "INFSIGHDR I---", "4:4:4"),
        ("INFSIGCOS 22", "INFSIGHDR IHDR10", "4:4:4/BT.2020"),
        ("INFSIGCOS 11", "INFSIGHDR IHDR10+", "4:2:2/BT.2020"),
        ("INFSIGCOS 11", "INFSIGHDR IDolby Vision", "4:2:2/BT.2020"),
        ("INFSIGCOS 99", "INFSIGHDR I---", "4:2:2/BT.2020"),
        ("INFSIGCOS 99", "INFSIGHDR IHDR10", "4:2:2/BT.2020"),
        ("INFSIGCOS 03", "INFSIGHDR IHDR10", None),
    ],
)
def test_colorspace_bt2020(colorspace, hdr, expected):
    """Test that BT.2020 is added for HDR if the receiver did not send it."""
    device = _device()
    device._ss_callback("Main", "SS", colorspace)
    device._ss_callback("Main", "SS", hdr)
    assert device.colorspace_input == expected


@pytest.mark.parametrize(
    "callback, attribute",
    [
        ("_sy_callback", "video_hdmi_signal_in"),
        ("_ss_callback", "audio_sampling_rate"),
        ("_ss_callback", "hdr_input"),
        ("_ss_callback", "pixel_depth_input"),
        ("_ss_callback", "max_frl_input"),
        ("_ss_callback", "colorspace_input"),
        ("_sy_callback", "max_resolution"),
        ("_sy_callback", "audio_signal"),
        ("_sy_callback", "audio_sound"),
        ("_op_callback", "input_channels"),
        ("_op_callback", "output_channels"),
    ],
)
def test_callbacks_ignore_other_events(callback, attribute):
    """Test that events with another prefix are ignored."""
    device = _device()
    getattr(device, callback)("Main", "SS", "TTR ON")
    assert getattr(device, attribute) is None


@pytest.mark.asyncio
async def test_trigger_sends_all_queries():
    """Test that all queries are sent without waiting for a confirmation."""
    device = _device()
    with (
        patch.object(
            type(device),
            "telnet_available",
            new_callable=PropertyMock,
            return_value=True,
        ),
        patch.object(
            device.telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_send,
        patch.object(asyncio, "sleep", new_callable=AsyncMock) as mock_sleep,
    ):
        await device.async_trigger_advanced_audio_video_info_update()

    # The protocol asks for at least 50 ms between commands
    assert [call.args[0] for call in mock_sleep.await_args_list] == [0.05] * 12
    commands = [call.args[0] for call in mock_send.call_args_list]
    assert len(commands) == 12
    assert "SSINFSIGRES ?" in commands
    assert "SYSMI ?" in commands
    assert all(
        call.kwargs == {"skip_confirmation": True, "background": True}
        for call in mock_send.call_args_list
    )


@pytest.mark.asyncio
async def test_trigger_without_telnet_sends_nothing():
    """Test that nothing is sent if telnet is not available."""
    device = _device()
    with patch.object(
        device.telnet_api, "async_send_commands", new_callable=AsyncMock
    ) as mock_send:
        await device.async_trigger_advanced_audio_video_info_update()

    mock_send.assert_not_called()


@pytest.mark.parametrize(
    "channel_status,expected",
    [
        ("00200000".ljust(32, "0"), "1.0"),
        ("22000000".ljust(32, "0"), "2.0"),
        ("22020000".ljust(32, "0"), "2.1"),
        ("22211111111111000000".ljust(32, "0"), "3.0"),
        ("20222000".ljust(32, "0"), "3.1"),
        ("22112211111111000000".ljust(32, "0"), "4.0"),
        ("22022200".ljust(32, "0"), "4.1"),
        ("22212211111111000000".ljust(32, "0"), "5.0"),
        ("22222211111111000000".ljust(32, "0"), "5.1"),
        ("22202220".ljust(32, "0"), "6.0"),
        ("22222211211111000000".ljust(32, "0"), "6.1"),
        ("22202222".ljust(32, "0"), "7.0"),
        ("22222222".ljust(32, "0"), "7.1"),
        ("22222211122111000000".ljust(32, "0"), "5.1.2"),
        ("22222211111112000000".ljust(32, "0"), "5.1.2"),
        ("22222211111112202000".ljust(32, "0"), "5.1.4"),
        ("22222222111111000000".ljust(32, "0"), "7.1"),
        ("22222222111111220000".ljust(32, "0"), "7.1.2"),
        ("22222222122112000000".ljust(32, "0"), "7.1.4"),
        ("22222222022000000000000002200000".ljust(32, "0"), "7.1.4"),
        ("22222222122112220000".ljust(32, "0"), "7.1.6"),
    ],
)
def test_channel_status_to_str(channel_status, expected):
    """Test channel_status_to_str function."""
    assert channel_status_to_str(channel_status) == expected
