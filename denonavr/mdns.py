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

from zeroconf import IPVersion, ServiceBrowser, ServiceInfo, ServiceListener, Zeroconf
from zeroconf.asyncio import AsyncZeroconf

from denonavr import DenonAVR

_LOGGER = logging.getLogger(__name__)


@dataclass
class ServiceInfoRecord:
    """Record for a discovered mDNS service."""

    name: str
    type: str
    info: ServiceInfo | None


class MDNSListener(ServiceListener):
    """Listener for mDNS service discovery."""

    def __init__(self):
        """Initialize the MDNSListener."""
        self.services: list[ServiceInfoRecord] = []
        self.lock = threading.Lock()

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Handle the addition of a new service."""
        info = zc.get_service_info(type_, name)
        with self.lock:
            self.services.append(ServiceInfoRecord(name=name, type=type_, info=info))
        _LOGGER.debug("Service %s added for type %s", name, type_)
        if info:
            _LOGGER.debug("Address: %s, Port: %s", info.parsed_addresses(), info.port)

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Handle the removal of a service."""
        with self.lock:
            self.services = [
                service
                for service in self.services
                if not (service.name == name and service.type == type_)
            ]
            _LOGGER.debug("Service %s removed for type %s", name, type_)

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Handle the update of an existing service."""
        info = zc.get_service_info(type_, name)
        with self.lock:
            for record in self.services:
                if record.name == name and record.type == type_:
                    record.info = info
                    break
            else:
                # If the service was not previously recorded, add it now.
                self.services.append(
                    ServiceInfoRecord(name=name, type=type_, info=info)
                )
        _LOGGER.debug("Service %s updated for type %s", name, type_)
        if info:
            _LOGGER.debug("Address: %s, Port: %s", info.parsed_addresses(), info.port)


async def async_query_receivers(timeout: float = 5) -> list[ServiceInfoRecord] | None:
    """
    Query for Denon/Marantz receivers using mDNS.

    Args:
        timeout: Number of seconds to wait for mDNS responses before
            collecting and returning the discovered services. During this
            period the service browser listens for receiver announcements.
    """
    async with AsyncZeroconf() as zeroconf:
        listener = MDNSListener()
        ServiceBrowser(zeroconf.zeroconf, "_heos-audio._tcp.local.", listener)

        await asyncio.sleep(timeout)
        with listener.lock:
            if not listener.services:
                return None

            services = []
            for service in listener.services:
                try:
                    ip_addresses = service.info.parsed_addresses(
                        version=IPVersion.V4Only
                    )
                    if not ip_addresses:
                        ip_addresses = service.info.parsed_addresses(
                            version=IPVersion.V6Only
                        )
                    if not ip_addresses:
                        _LOGGER.info(
                            "No IP address found for service %s (%s)",
                            service.name,
                            service.type,
                        )
                        continue
                    device = DenonAVR(ip_addresses[0])
                    await device.async_setup()
                    services.append(service)
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.info(
                        "Failed to set up receiver for service %s (%s)",
                        service.name,
                        service.type,
                        exc_info=True,
                    )
            return services or None
