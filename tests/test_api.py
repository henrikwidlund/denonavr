#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module covers some basic automated tests for the api module.

:copyright: (c) 2016 by Oliver Goetz.
:license: MIT, see LICENSE for more details.
"""

# pylint: disable=protected-access

import asyncio

import pytest

from denonavr.api import (
    _EVENTS_PRODUCING_DUPLICATES,
    DenonAVRTelnetApi,
    _should_propagate_event,
)


def test_should_propagate_event_initial():
    """Test that the event is propagated when the tracker is empty."""
    for duplicate_key in _EVENTS_PRODUCING_DUPLICATES:
        tracker = {k: "" for k in _EVENTS_PRODUCING_DUPLICATES}
        parameter = duplicate_key + "_new"
        assert _should_propagate_event("TEST_EVENT", parameter, tracker)
        assert tracker[duplicate_key] == parameter


def test_should_propagate_event_duplicate():
    """Test that the event is not propagated when the tracker has the same parameter."""
    for duplicate_key in _EVENTS_PRODUCING_DUPLICATES:
        tracker = {k: "" for k in _EVENTS_PRODUCING_DUPLICATES}
        parameter = duplicate_key + "_val"
        assert _should_propagate_event("EV", parameter, tracker)
        assert not _should_propagate_event("EV", parameter, tracker)
        new_param = duplicate_key + "_val2"
        assert _should_propagate_event("EV", new_param, tracker)
        assert tracker[duplicate_key] == new_param


def test_should_propagate_event_no_match():
    """Test that the event is propagated when the parameter is not a duplicate key."""
    tracker = {k: "" for k in _EVENTS_PRODUCING_DUPLICATES}
    assert _should_propagate_event("EV", "UNRELATED_PARAM", tracker)
    assert all(value == "" for value in tracker.values())


def test_duplicate_event_cache_propagation():
    """Test duplicate event suppression and cache clearing in DenonAVRTelnetApi."""
    api = DenonAVRTelnetApi()
    duplicate_key = next(iter(_EVENTS_PRODUCING_DUPLICATES))
    param1 = duplicate_key + "_val1"
    param2 = duplicate_key + "_val1"  # duplicate

    assert _should_propagate_event("EV", param1, api._potential_duplicate_events)
    assert not _should_propagate_event("EV", param2, api._potential_duplicate_events)
    api.clear_duplicate_event_cache()
    assert _should_propagate_event("EV", param1, api._potential_duplicate_events)


class _ProtocolFake:
    """Telnet protocol that records written commands."""

    connected = True

    def __init__(self) -> None:
        """Create an empty record."""
        self.written: list[str] = []

    def write(self, data: str) -> None:
        """Record a command."""
        self.written.append(data.strip())


def _connected_telnet_api() -> DenonAVRTelnetApi:
    api = DenonAVRTelnetApi()
    api._connection_enabled = True
    api._protocol = _ProtocolFake()
    api._rate_limiter.enabled = False
    return api


@pytest.mark.asyncio
async def test_background_command_waits_for_user_command(monkeypatch):
    """Test that background commands are sent after pending user commands."""
    monkeypatch.setattr("denonavr.api._BACKGROUND_PAUSE_AFTER_COMMAND", 0.05)
    api = _connected_telnet_api()
    release = asyncio.Event()

    async def wait_for_confirmation():
        await release.wait()

    monkeypatch.setattr(api._send_confirmation_event, "wait", wait_for_confirmation)
    user = asyncio.create_task(api.async_send_commands("MVUP"))
    await asyncio.sleep(0)
    background = asyncio.create_task(
        api.async_send_commands("MV?", skip_confirmation=True, background=True)
    )
    await asyncio.sleep(0.01)

    assert api._protocol.written == ["MVUP"]

    release.set()
    await user
    await asyncio.sleep(0.01)
    # Still paused right after the user command
    assert api._protocol.written == ["MVUP"]

    await background
    assert api._protocol.written == ["MVUP", "MV?"]


@pytest.mark.asyncio
async def test_background_command_is_sent_without_user_commands():
    """Test that background commands are sent at once when idle."""
    api = _connected_telnet_api()

    await api.async_send_commands("MV?", skip_confirmation=True, background=True)

    assert api._protocol.written == ["MV?"]
