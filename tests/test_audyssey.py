#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module covers some basic automated tests of audyssey.

:copyright: (c) 2016 by Oliver Goetz.
:license: MIT, see LICENSE for more details.
"""

from unittest.mock import AsyncMock, patch

import pytest

from denonavr.api import DenonAVRApi, DenonAVRTelnetApi
from denonavr.audyssey import AvrCommandError, DenonAVRAudyssey
from denonavr.const import REF_LVL_OFFSET_MAP_LABELS_TELNET
from denonavr.foundation import DenonAVRDeviceInfo
from tests.test_helpers import patch_telnet_available

VALID_REFLEV = next(iter(REF_LVL_OFFSET_MAP_LABELS_TELNET.keys()))


class TestDenonAVRAudyssey:
    """Test case for DenonAVRAudyssey class."""

    @pytest.mark.asyncio
    async def test_async_dynamiceq_on_returns_early_when_on(self):
        """Test that no command is sent when DynamicEQ is already on."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        # Set state using correct callback format
        device._ps_callback("Main", "", "DYNEQ ON")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_command, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_dynamiceq_on()
            mock_get_command.assert_not_called()
            mock_post_command.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_dynamiceq_on_sends_command_when_off(self):
        """Test that command is sent when DynamicEQ is off."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "DYNEQ OFF")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_command, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_dynamiceq_on()
            assert (
                mock_get_command.call_count
                + mock_telnet.call_count
                + mock_post_command.call_count
                == 1
            )

    @pytest.mark.asyncio
    async def test_async_dynamiceq_off_returns_early_when_off(self):
        """Test that no command is sent when DynamicEQ is already off."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "DYNEQ OFF")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_command, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_dynamiceq_off()
            mock_get_command.assert_not_called()
            mock_post_command.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_dynamiceq_off_sends_command_when_on(self):
        """Test that command is sent when DynamicEQ is on."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "DYNEQ ON")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_command, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_dynamiceq_off()
            assert (
                mock_get_command.call_count
                + mock_telnet.call_count
                + mock_post_command.call_count
                == 1
            )

    @pytest.mark.asyncio
    async def test_async_set_reflevoffset_raises_if_dynamiceq_off(self):
        """Test that setting reflev offset raises error if DynamicEQ is off."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "DYNEQ OFF")
        with patch_telnet_available(device_info):
            with pytest.raises(AvrCommandError):
                await device.async_set_reflevoffset(VALID_REFLEV)

    @pytest.mark.asyncio
    async def test_async_set_reflevoffset_returns_early_when_matches(self):
        """Test that no command is sent when reflev offset matches."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "DYNEQ ON")
        # Use the mapped value for _reflevoffset, as would be set by the callback
        mapped_value = list(REF_LVL_OFFSET_MAP_LABELS_TELNET.values())[0]
        test_key = list(REF_LVL_OFFSET_MAP_LABELS_TELNET.keys())[0]
        device._ps_callback("Main", "", f"REFLEV {mapped_value}")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_command, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_set_reflevoffset(test_key)
            mock_get_command.assert_not_called()
            mock_post_command.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_set_reflevoffset_sends_command_when_differs(self):
        """Test that command is sent when reflev offset differs."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "DYNEQ ON")
        all_keys = list(REF_LVL_OFFSET_MAP_LABELS_TELNET.keys())
        all_values = list(REF_LVL_OFFSET_MAP_LABELS_TELNET.values())
        test_val = all_keys[1] if len(all_keys) > 1 else all_keys[0]
        device._ps_callback("Main", "", f"REFLEV {all_values[0]}")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_command, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_set_reflevoffset(test_val)
            assert (
                mock_get_command.call_count
                + mock_telnet.call_count
                + mock_post_command.call_count
                == 1
            )

    @pytest.mark.asyncio
    async def test_async_lfc_on_returns_early_when_on(self):
        """Test that no command is sent when LFC is already on."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "LFC ON")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_command, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_lfc_on()
            mock_get_command.assert_not_called()
            mock_post_command.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_lfc_on_sends_command_when_off(self):
        """Test that command is sent when LFC is off."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "LFC OFF")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_command, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_lfc_on()
            assert (
                mock_get_command.call_count
                + mock_telnet.call_count
                + mock_post_command.call_count
                == 1
            )

    @pytest.mark.asyncio
    async def test_async_lfc_off_returns_early_when_off(self):
        """Test that no command is sent when LFC is already off."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "LFC OFF")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_command, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_lfc_off()
            mock_get_command.assert_not_called()
            mock_post_command.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_lfc_off_sends_command_when_on(self):
        """Test that command is sent when LFC is on."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "LFC ON")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_command, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_lfc_off()
            assert (
                mock_get_command.call_count
                + mock_telnet.call_count
                + mock_post_command.call_count
                == 1
            )

    @pytest.mark.asyncio
    async def test_async_containment_amount_returns_early_when_matches(self):
        """Test that no command is sent when containment amount matches."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "CNTAMT 3")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_command, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_containment_amount(3)
            mock_get_command.assert_not_called()
            mock_post_command.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_containment_amount_sends_command_when_differs(self):
        """Test that command is sent when containment amount differs."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "CNTAMT 2")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_command, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_containment_amount(3)
            assert (
                mock_get_command.call_count
                + mock_telnet.call_count
                + mock_post_command.call_count
                == 1
            )

    @pytest.mark.asyncio
    async def test_async_containment_amount_raises_on_invalid(self):
        """Test that setting invalid containment amount raises error."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        with patch_telnet_available(device_info):
            with pytest.raises(AvrCommandError):
                await device.async_containment_amount(0)
            with pytest.raises(AvrCommandError):
                await device.async_containment_amount(8)

    @pytest.mark.asyncio
    async def test_async_set_multieq_returns_early_when_matches(self):
        """Test that no command is sent when MultiEQ setting matches."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        # Use a valid MultiEQ value from the mapping
        from denonavr.const import MULTI_EQ_MAP_LABELS_TELNET

        valid_key = next(iter(MULTI_EQ_MAP_LABELS_TELNET.keys()))
        valid_value = MULTI_EQ_MAP_LABELS_TELNET[valid_key]
        device._ps_callback("Main", "", f"MULTEQ:{valid_value}")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_appcommand, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_set_multieq(valid_key)
            mock_get_command.assert_not_called()
            mock_post_appcommand.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_set_multieq_sends_command_when_differs(self):
        """Test that command is sent when MultiEQ setting differs."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        from denonavr.const import MULTI_EQ_MAP_LABELS_TELNET

        all_keys = list(MULTI_EQ_MAP_LABELS_TELNET.keys())
        all_values = list(MULTI_EQ_MAP_LABELS_TELNET.values())
        test_key = all_keys[1] if len(all_keys) > 1 else all_keys[0]
        device._ps_callback("Main", "", f"MULTEQ:{all_values[0]}")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_appcommand, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_set_multieq(test_key)
            assert (
                mock_get_command.call_count
                + mock_post_appcommand.call_count
                + mock_telnet.call_count
                == 1
            )

    @pytest.mark.asyncio
    async def test_async_set_multieq_raises_on_invalid(self):
        """Test that setting invalid MultiEQ raises error."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        with patch_telnet_available(device_info), patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ):
            with pytest.raises(AvrCommandError):
                await device.async_set_multieq("notavalidmode")

    @pytest.mark.asyncio
    async def test_async_set_dynamicvol_returns_early_when_matches(self):
        """Test that no command is sent when Dynamic Volume setting matches."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        from denonavr.const import DYNAMIC_VOLUME_MAP_LABELS_TELNET

        valid_key = next(iter(DYNAMIC_VOLUME_MAP_LABELS_TELNET.keys()))
        valid_value = DYNAMIC_VOLUME_MAP_LABELS_TELNET[valid_key]
        device._ps_callback("Main", "", f"DYNVOL {valid_value}")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_appcommand, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_set_dynamicvol(valid_key)
            mock_get_command.assert_not_called()
            mock_post_appcommand.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_set_dynamicvol_sends_command_when_differs(self):
        """Test that command is sent when Dynamic Volume setting differs."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        from denonavr.const import DYNAMIC_VOLUME_MAP_LABELS_TELNET

        all_keys = list(DYNAMIC_VOLUME_MAP_LABELS_TELNET.keys())
        all_values = list(DYNAMIC_VOLUME_MAP_LABELS_TELNET.values())
        test_key = all_keys[1] if len(all_keys) > 1 else all_keys[0]
        device._ps_callback("Main", "", f"DYNVOL {all_values[0]}")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_appcommand, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_set_dynamicvol(test_key)
            assert (
                mock_get_command.call_count
                + mock_post_appcommand.call_count
                + mock_telnet.call_count
                == 1
            )

    @pytest.mark.asyncio
    async def test_async_set_dynamicvol_raises_on_invalid(self):
        """Test that setting invalid Dynamic Volume raises error."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        with patch_telnet_available(device_info), patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ):
            with pytest.raises(AvrCommandError):
                await device.async_set_dynamicvol("notavalidmode")

    @pytest.mark.asyncio
    async def test_async_containment_amount_up_returns_early_when_max(self):
        """Test that no command is sent when containment amount is at max."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "CNTAMT 7")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_appcommand, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_containment_amount_up()
            mock_get_command.assert_not_called()
            mock_post_appcommand.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_containment_amount_up_sends_command_when_not_max(self):
        """Test that command is sent when containment amount is not at max."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "CNTAMT 5")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_appcommand, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_containment_amount_up()
            assert (
                mock_get_command.call_count
                + mock_post_appcommand.call_count
                + mock_telnet.call_count
                == 1
            )

    @pytest.mark.asyncio
    async def test_async_containment_amount_down_returns_early_when_min(self):
        """Test that no command is sent when containment amount is at min."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "CNTAMT 1")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_appcommand, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_containment_amount_down()
            mock_get_command.assert_not_called()
            mock_post_appcommand.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_containment_amount_down_sends_command_when_not_min(self):
        """Test that command is sent when containment amount is not at min."""
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRAudyssey(device=device_info)
        device._ps_callback("Main", "", "CNTAMT 3")
        with patch_telnet_available(device_info), patch.object(
            api, "async_get_command", new_callable=AsyncMock
        ) as mock_get_command, patch.object(
            api, "async_post_appcommand", new_callable=AsyncMock
        ) as mock_post_appcommand, patch.object(
            telnet_api, "async_send_commands", new_callable=AsyncMock
        ) as mock_telnet:
            await device.async_containment_amount_down()
            assert (
                mock_get_command.call_count
                + mock_post_appcommand.call_count
                + mock_telnet.call_count
                == 1
            )
