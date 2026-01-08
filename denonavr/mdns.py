#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module implements a discovery function for Denon AVR receivers via mDNS.

:copyright: (c) 2025 by Henrik Widlund.
:license: MIT, see LICENSE for more details.
"""

import asyncio
import logging
import threading
from dataclasses import dataclass
from typing import List, Optional

from zeroconf import ServiceBrowser, ServiceInfo, ServiceListener
from zeroconf.asyncio import AsyncZeroconf

_LOGGER = logging.getLogger(__name__)


@dataclass
class ServiceInfoRecord:
    """Record for a discovered mDNS service."""

    name: str
    type: str
    info: Optional[ServiceInfo]


class MDNSListener(ServiceListener):
    """Listener for mDNS service discovery."""

    def __init__(self):
        """Initialize the MDNSListener."""
        self.services: List[ServiceInfoRecord] = []
        self.lock = threading.Lock()

    def add_service(self, zc, type_, name):
        """Handle the addition of a new service."""
        info = zc.get_service_info(type_, name)
        with self.lock:
            self.services.append(ServiceInfoRecord(name=name, type=type_, info=info))
        _LOGGER.debug("Service %s added for type %s", name, type_)
        if info:
            _LOGGER.debug("Address: %s, Port: %s", info.parsed_addresses(), info.port)

    def update_service(self, zc, type_, name):
        """Handle the update of an existing service."""
        _LOGGER.debug("Service %s updated for type %s", name, type_)

    def remove_service(self, zc, type_, name):
        """Handle the removal of a service."""
        _LOGGER.debug("Service %s removed for type %s", name, type_)

    @staticmethod
    async def query_receivers(timeout=5) -> Optional[List[ServiceInfoRecord]]:
        """Query for Denon/Marantz receivers using mDNS."""
        async with AsyncZeroconf() as zeroconf:
            listener = MDNSListener()
            ServiceBrowser(zeroconf.zeroconf, "_heos-audio._tcp.local.", listener)

            await asyncio.sleep(timeout)
            return listener.services
