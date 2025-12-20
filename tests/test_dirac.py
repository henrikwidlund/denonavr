#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module covers some basic automated tests of dirac.

:copyright: (c) 2016 by Oliver Goetz.
:license: MIT, see LICENSE for more details.
"""
from unittest.mock import AsyncMock, patch

import pytest

from denonavr.api import DenonAVRApi, DenonAVRTelnetApi
from denonavr.const import DIRAC_FILTER_MAP
from denonavr.dirac import DenonAVRDirac
from denonavr.exceptions import AvrCommandError
from denonavr.foundation import DenonAVRDeviceInfo
from tests.test_helpers import patch_telnet_available


class TestDenonAVRDirac:
    """Tests for DenonAVRDirac Dirac filter logic."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("filter_val", list(DIRAC_FILTER_MAP.keys()))
    async def test_async_dirac_filter_returns_early_when_matches(self, filter_val):
        """Test that async_dirac_filter returns early when same filter."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRDirac(device=device_info)
        mapped = DIRAC_FILTER_MAP[filter_val]
        assert mapped is not None, f"Mapping for {filter_val} should not be None"
        device._ps_callback("Main", "", f"DIRAC:{mapped}")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_dirac_filter(filter_val)
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "from_val,to_val",
        [
            ("Off", "Slot 1"),
            ("Slot 1", "Slot 2"),
            ("Slot 2", "Slot 3"),
            ("Slot 3", "Off"),
        ],
    )
    async def test_async_dirac_filter_sends_command_when_differs(
        self, from_val, to_val
    ):
        """Test that async_dirac_filter sends command when filter differs."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRDirac(device=device_info)
        mapped = DIRAC_FILTER_MAP[from_val]
        assert mapped is not None, f"Mapping for {from_val} should not be None"
        device._ps_callback("Main", "", f"DIRAC {mapped}")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_dirac_filter(to_val)  # type: ignore
            assert (
                mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1
            )

    @pytest.mark.asyncio
    async def test_async_dirac_filter_raises_on_invalid(self):
        """Test that async_dirac_filter raises on invalid filter."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRDirac(device=device_info)
        with patch_telnet_available(device_info), patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ):
            with pytest.raises(AvrCommandError):
                await device.async_dirac_filter("notavalidfilter")  # type: ignore
