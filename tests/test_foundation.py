import pytest
from unittest.mock import AsyncMock, patch
from denonavr.foundation import DenonAVRDeviceInfo, AvrCommandError
from denonavr.api import DenonAVRApi, DenonAVRTelnetApi

@pytest.mark.asyncio
async def test_async_power_on_returns_early_when_power_is_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._power_callback("Main", "PW", "ON")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_power_on()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_power_on_sends_command_when_power_is_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._power_callback("Main", "PW", "OFF")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_power_on()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_power_off_returns_early_when_power_is_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._power_callback("Main", "PW", "OFF")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_power_off()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_power_off_sends_command_when_power_is_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._power_callback("Main", "PW", "ON")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_power_off()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_sleep_returns_early_when_sleep_matches():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._auto_sleep_callback("Main", "SLP", "030")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_sleep(30)
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_sleep_sends_command_when_sleep_differs():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._auto_sleep_callback("Main", "SLP", "010")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_sleep(30)
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_sleep_returns_early_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._auto_sleep_callback("Main", "SLP", "OFF")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_sleep("OFF")
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_sleep_sends_command_when_not_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._auto_sleep_callback("Main", "SLP", "030")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_sleep("OFF")
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_room_size_returns_early_when_matches():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._room_size_callback("ROOMS")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_room_size("S")
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_room_size_sends_command_when_differs():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._room_size_callback("ROOMS")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_room_size("M")
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_room_size_raises_on_invalid():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._room_size_callback("ROOMS")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        with pytest.raises(AvrCommandError):
            await device.async_room_size("INVALID")
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_tactile_transducer_on_returns_early_when_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._tactile_transducer_callback("TTR ON")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_tactile_transducer_on()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_tactile_transducer_on_sends_command_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._tactile_transducer_callback("TTR OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_tactile_transducer_on()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_tactile_transducer_off_returns_early_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._tactile_transducer_callback("TTR OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_tactile_transducer_off()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_tactile_transducer_off_sends_command_when_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._tactile_transducer_callback("TTR ON")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_tactile_transducer_off()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_trigger_on_returns_early_when_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._trigger_callback("Main", "TRG", "1 ON")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_trigger_on(1)
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_trigger_on_sends_command_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._trigger_callback("Main", "TRG", "1 OFF")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_trigger_on(1)
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_trigger_off_returns_early_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._trigger_callback("Main", "TRG", "1 OFF")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_trigger_off(1)
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_trigger_off_sends_command_when_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._trigger_callback("Main", "TRG", "1 ON")
    with patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_trigger_off(1)
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_delay_up_returns_early_when_max():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._delay_callback("DELAY 500")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_delay_up()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_delay_up_sends_command_when_not_max():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._delay_callback("DELAY 100")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_delay_up()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_delay_down_returns_early_when_min():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._delay_callback("DELAY 000")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_delay_down()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_delay_down_sends_command_when_not_min():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._delay_callback("DELAY 100")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_delay_down()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_delay_returns_early_when_matches():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._delay_callback("DELAY 100")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_delay(100)
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_delay_sends_command_when_differs():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._delay_callback("DELAY 100")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_delay(200)
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_eco_mode_returns_early_when_matches():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._eco_mode_callback("Main", "ECO", "ON")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_eco_mode("On")
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_eco_mode_sends_command_when_differs():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._eco_mode_callback("Main", "ECO", "AUTO")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_eco_mode("On")
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_eco_mode_raises_on_invalid():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._eco_mode_callback("Main", "ECO", "On")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        with pytest.raises(AvrCommandError):
            await device.async_eco_mode("InvalidMode")

@pytest.mark.asyncio
async def test_async_hdmi_output_returns_early_when_matches():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._hdmi_output_callback("MONI1")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_hdmi_output("HDMI1")
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_hdmi_output_sends_command_when_differs():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._hdmi_output_callback("MONIAUTO")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_hdmi_output("HDMI2")
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_hdmi_output_raises_on_invalid():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._hdmi_output_callback("MONI1")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        with pytest.raises(AvrCommandError):
            await device.async_hdmi_output("InvalidOutput")

@pytest.mark.asyncio
async def test_async_hdmi_audio_decode_returns_early_when_matches():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._hdmi_audio_decode_callback("AUDIO AMP")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_hdmi_audio_decode("AMP")
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_hdmi_audio_decode_sends_command_when_differs():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._hdmi_audio_decode_callback("AUDIO AMP")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_hdmi_audio_decode("TV")
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_hdmi_audio_decode_raises_on_invalid():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._hdmi_audio_decode_callback("Auto")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        with pytest.raises(AvrCommandError):
            await device.async_hdmi_audio_decode("InvalidMode")

@pytest.mark.asyncio
async def test_async_video_processing_mode_returns_early_when_matches():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._video_processing_mode_callback("VPMAUTO")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_video_processing_mode("Auto")
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_video_processing_mode_sends_command_when_differs():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._video_processing_mode_callback("VPMAUTO")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_video_processing_mode("Movie")
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_video_processing_mode_raises_on_invalid():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._video_processing_mode_callback("VPMAUTO")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        with pytest.raises(AvrCommandError):
            await device.async_video_processing_mode("InvalidMode")

@pytest.mark.asyncio
async def test_async_speaker_preset_returns_early_when_matches():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._speaker_preset_callback("Main", "SP", "PR 1")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_speaker_preset(1)
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_speaker_preset_sends_command_when_differs():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._ss_callback("Main", "SSPST", "1")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_speaker_preset(2)
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_speaker_preset_raises_on_invalid():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._ss_callback("Main", "SSPST", "1")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        with pytest.raises(AvrCommandError):
            await device.async_speaker_preset(42)

@pytest.mark.asyncio
async def test_async_bt_transmitter_on_returns_early_when_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._bt_callback("Main", "BT", "TX ON")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_bt_transmitter_on()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_bt_transmitter_on_sends_command_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._bt_callback("Main", "BT", "TX OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_bt_transmitter_on()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_bt_transmitter_off_returns_early_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._bt_callback("Main", "BT", "TX OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_bt_transmitter_off()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_bt_transmitter_off_sends_command_when_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._bt_callback("Main", "BT", "TX ON")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_bt_transmitter_off()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_delay_time_up_returns_early_when_max():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._delay_time_callback("DEL 300")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_delay_time_up()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_delay_time_up_sends_command_when_not_max():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._delay_time_callback("DEL 100")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_delay_time_up()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_delay_time_down_returns_early_when_min():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._delay_time_callback("DEL 000")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_delay_time_down()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_delay_time_down_sends_command_when_not_min():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._delay_time_callback("DEL 100")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_delay_time_down()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_delay_time_returns_early_when_matches():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._delay_time_callback("DEL 100")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_delay_time(100)
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_delay_time_sends_command_when_differs():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._delay_time_callback("DELAYT 100")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_delay_time(200)
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_audio_restorer_low_returns_early_when_low():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._audio_restorer_callback("RSTR LOW")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_audio_restorer("Low")
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_audio_restorer_low_sends_command_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._audio_restorer_callback("RSTR OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_audio_restorer("Low")
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_graphic_eq_on_returns_early_when_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._graphic_eq_callback("GEQ ON")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_graphic_eq_on()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_graphic_eq_on_sends_command_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._graphic_eq_callback("GEQ OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_graphic_eq_on()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_graphic_eq_off_returns_early_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._graphic_eq_callback("GEQ OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_graphic_eq_off()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_graphic_eq_off_sends_command_when_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._graphic_eq_callback("GEQ ON")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_graphic_eq_off()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_headphone_eq_on_returns_early_when_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._headphone_eq_callback("HEQ ON")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_headphone_eq_on()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_headphone_eq_on_sends_command_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._headphone_eq_callback("HEQ OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_headphone_eq_on()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_headphone_eq_off_returns_early_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._headphone_eq_callback("HEQ OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_headphone_eq_off()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_headphone_eq_off_sends_command_when_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._headphone_eq_callback("HEQ ON")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_headphone_eq_off()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_illumination_returns_early_when_matches():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device.manufacturer = "Marantz"
    device._illumination_callback("Main", "", "ILL AUTO")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_illumination("Auto")
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_illumination_sends_command_when_differs():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device.manufacturer = "Marantz"
    device._illumination_callback("Main", "", "ILL AUTO")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_illumination("Off")
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_illumination_raises_on_invalid():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device.manufacturer = "Marantz"
    device._illumination_callback("Main", "", "ILL AUTO")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        with pytest.raises(AvrCommandError):
            await device.async_illumination("InvalidState")

@pytest.mark.asyncio
async def test_async_auto_lip_sync_on_returns_early_when_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device.manufacturer = "Marantz"
    device._auto_lip_sync_callback("HOS ON")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_auto_lip_sync_on()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_auto_lip_sync_on_sends_command_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device.manufacturer = "Marantz"
    device._auto_lip_sync_callback("HOS OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_auto_lip_sync_on()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_auto_lip_sync_off_returns_early_when_off():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device.manufacturer = "Marantz"
    device._auto_lip_sync_callback("HOS OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_auto_lip_sync_off()
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_auto_lip_sync_off_sends_command_when_on():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device.manufacturer = "Marantz"
    device._auto_lip_sync_callback("HOS ON")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_auto_lip_sync_off()
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_bt_output_mode_returns_early_when_matches():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._bt_callback("Main", "", "TX SP")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_bt_output_mode("Bluetooth + Speakers")
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_bt_output_mode_sends_command_when_differs():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._bt_callback("Main", "", "TX SP")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_bt_output_mode("Bluetooth Only")
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_bt_output_mode_raises_on_invalid():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._bt_callback("Main", "", "TX SP")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        with pytest.raises(AvrCommandError):
            await device.async_bt_output_mode("INVALID")

@pytest.mark.asyncio
async def test_async_audio_restorer_returns_early_when_matches():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._audio_restorer_callback("RSTR OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_audio_restorer("Off")
        mock_get_command.assert_not_called()

@pytest.mark.asyncio
async def test_async_audio_restorer_sends_command_when_differs():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._audio_restorer_callback("RSTR OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        await device.async_audio_restorer("High")
        mock_get_command.assert_called_once()

@pytest.mark.asyncio
async def test_async_audio_restorer_raises_on_invalid():
    api = DenonAVRApi()
    telnet_api = DenonAVRTelnetApi()
    device = DenonAVRDeviceInfo(api=api, telnet_api=telnet_api, zone="Main")
    device._audio_restorer_callback("RSTR OFF")
    with patch.object(device.telnet_api.__class__, "connected", new=property(lambda self: False)), \
         patch.object(device.telnet_api.__class__, "healthy", new=property(lambda self: False)), \
         patch.object(api, "async_get_command", new_callable=AsyncMock) as mock_get_command:
        with pytest.raises(AvrCommandError):
            await device.async_audio_restorer("Max")
