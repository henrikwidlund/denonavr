#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for DenonAVRSoundMode (sound mode logic).
"""
import pytest
from unittest.mock import AsyncMock, patch
from denonavr.soundmode import DenonAVRSoundMode
from denonavr.api import DenonAVRApi, DenonAVRTelnetApi
from denonavr.foundation import DenonAVRDeviceInfo
from tests.test_helpers import patch_telnet_available
from denonavr.const import (
    AURO_MATIC_3D_PRESET_MAP_LABELS,
    MDAX_MAP_LABELS,
    DAC_FILTERS_MAP_LABELS,
    DIALOG_ENHANCER_LEVEL_MAP_LABELS,
)

class TestDenonAVRSoundMode:
    @pytest.mark.asyncio
    async def test_async_neural_x_on_returns_early_when_on(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "NEURAL:ON")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_neural_x_on()
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_neural_x_on_sends_command_when_off(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "NEURAL:OFF")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_neural_x_on()
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_neural_x_off_returns_early_when_off(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "NEURAL:OFF")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_neural_x_off()
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_neural_x_off_sends_command_when_on(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "NEURAL:ON")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_neural_x_off()
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_imax_auto_returns_early_when_auto(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAX AUTO")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_auto()
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_imax_auto_sends_command_when_not_auto(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAX OFF")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_auto()
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_imax_off_returns_early_when_off(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAX OFF")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_off()
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_imax_off_sends_command_when_not_off(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAX AUTO")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_off()
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_cinema_eq_on_returns_early_when_on(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "CINEMA EQ.ON")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_cinema_eq_on()
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_cinema_eq_on_sends_command_when_off(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "CINEMA EQ.OFF")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_cinema_eq_on()
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_cinema_eq_off_returns_early_when_off(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "CINEMA EQ.OFF")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_cinema_eq_off()
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_cinema_eq_off_sends_command_when_on(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "CINEMA EQ.ON")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_cinema_eq_off()
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_imax_audio_settings_returns_early_when_matches(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAXAUD AUTO")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_audio_settings("AUTO")
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_imax_audio_settings_sends_command_when_differs(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAXAUD MANUAL")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_audio_settings("AUTO")
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_imax_hpf_returns_early_when_matches(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAXHPF 080")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_hpf(80)
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_imax_hpf_sends_command_when_differs(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAXHPF 060")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_hpf(80)
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_imax_lpf_returns_early_when_matches(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAXLPF 120")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_lpf(120)
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_imax_lpf_sends_command_when_differs(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAXLPF 80")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_lpf(120)
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_imax_subwoofer_mode_returns_early_when_matches(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAXSWM ON")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_subwoofer_mode("ON")
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_imax_subwoofer_mode_sends_command_when_differs(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAXSWM OFF")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_subwoofer_mode("ON")
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_imax_subwoofer_output_returns_early_when_matches(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAXSWO L+M")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_subwoofer_output("L+M")
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_imax_subwoofer_output_sends_command_when_differs(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        device._ps_callback("Main", "", "IMAXSWO LFE")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_imax_subwoofer_output("L+M")
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_dialog_enhancer_returns_early_when_matches(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        # Use a valid dialog enhancer level from the mapping
        level = next(iter(DIALOG_ENHANCER_LEVEL_MAP_LABELS.keys()))
        mapped = DIALOG_ENHANCER_LEVEL_MAP_LABELS[level]
        device._ps_callback("Main", "", f"DEH {level}")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_dialog_enhancer(mapped)
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_dialog_enhancer_sends_command_when_differs(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        # Use two valid dialog enhancer levels from the mapping
        levels = list(DIALOG_ENHANCER_LEVEL_MAP_LABELS.keys())
        mapped1 = DIALOG_ENHANCER_LEVEL_MAP_LABELS[levels[0]]
        mapped2 = DIALOG_ENHANCER_LEVEL_MAP_LABELS[levels[1]] if len(levels) > 1 else mapped1
        device._ps_callback("Main", "", f"DEH {levels[0]}")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_dialog_enhancer(mapped2)
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_auromatic_3d_preset_returns_early_when_matches(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        # Use a valid preset from the mapping
        preset = next(iter(AURO_MATIC_3D_PRESET_MAP_LABELS.keys()))
        mapped = AURO_MATIC_3D_PRESET_MAP_LABELS[preset]
        device._ps_callback("Main", "", f"AUROPR {preset}")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_auromatic_3d_preset(mapped)
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_auromatic_3d_preset_sends_command_when_differs(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device = DenonAVRSoundMode(device=device_info)
        presets = list(AURO_MATIC_3D_PRESET_MAP_LABELS.keys())
        mapped1 = AURO_MATIC_3D_PRESET_MAP_LABELS[presets[0]]
        mapped2 = AURO_MATIC_3D_PRESET_MAP_LABELS[presets[1]] if len(presets) > 1 else mapped1
        device._ps_callback("Main", "", f"AUROPR {presets[0]}")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_auromatic_3d_preset(mapped2)
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_mdax_returns_early_when_matches(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device_info.manufacturer ="Marantz"
        device = DenonAVRSoundMode(device=device_info)
        # Use a valid MDAX value from the mapping
        mdax = next(iter(MDAX_MAP_LABELS.keys()))
        mapped = MDAX_MAP_LABELS[mdax]
        device._ps_callback("Main", "", f"MDAX {mdax}")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_mdax(mapped)
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_mdax_sends_command_when_differs(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device_info.manufacturer ="Marantz"
        device = DenonAVRSoundMode(device=device_info)
        mdaxs = list(MDAX_MAP_LABELS.keys())
        mapped1 = MDAX_MAP_LABELS[mdaxs[0]]
        mapped2 = MDAX_MAP_LABELS[mdaxs[1]] if len(mdaxs) > 1 else mapped1
        device._ps_callback("Main", "", f"MDAX {mdaxs[0]}")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_mdax(mapped2)
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1

    @pytest.mark.asyncio
    async def test_async_dac_filter_returns_early_when_matches(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device_info.manufacturer ="Marantz"
        device = DenonAVRSoundMode(device=device_info)
        # Use a valid DAC filter value from the mapping
        dac = next(iter(DAC_FILTERS_MAP_LABELS.keys()))
        mapped = DAC_FILTERS_MAP_LABELS[dac]
        device._ps_callback("Main", "", f"DACFIL {dac}")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_dac_filter(mapped)
            mock_get.assert_not_called()
            mock_post.assert_not_called()
            mock_telnet.assert_not_called()

    @pytest.mark.asyncio
    async def test_async_dac_filter_sends_command_when_differs(self):
        api = DenonAVRApi()
        telnet_api = DenonAVRTelnetApi()
        device_info = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
        device_info.manufacturer ="Marantz"
        device = DenonAVRSoundMode(device=device_info)
        dacs = list(DAC_FILTERS_MAP_LABELS.keys())
        mapped1 = DAC_FILTERS_MAP_LABELS[dacs[0]]
        mapped2 = DAC_FILTERS_MAP_LABELS[dacs[1]] if len(dacs) > 1 else mapped1
        device._ps_callback("Main", "", f"DACFIL {dacs[0]}")
        with patch_telnet_available(device_info), \
             patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get, \
             patch.object(api, "async_post_appcommand", new_callable=AsyncMock) as mock_post, \
             patch.object(telnet_api, "async_send_commands", new_callable=AsyncMock) as mock_telnet:
            await device.async_dac_filter(mapped2)
            assert mock_get.call_count + mock_post.call_count + mock_telnet.call_count == 1
