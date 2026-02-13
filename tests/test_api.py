#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module covers some basic automated tests for the api module.

:copyright: (c) 2016 by Oliver Goetz.
:license: MIT, see LICENSE for more details.
"""

# pylint: disable=protected-access

from denonavr.api import _EVENTS_PRODUCING_DUPLICATES, _should_propagate_event


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
