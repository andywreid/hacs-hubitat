import asyncio
from enum import Enum
from typing import (
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    NamedTuple,
    Optional,
    Protocol,
    Set,
    TypeVar,
)

import voluptuous as vol

from homeassistant.config_entries import ConfigEntries
from homeassistant.helpers.device_registry import DeviceRegistry

# Create proper typing for HA's callback decorator
T = TypeVar("T")
callback: Callable[[T], T]

class Context: ...

class StateMachine:
    def async_set(
        self,
        entity_id: str,
        new_state: str,
        attributes: Optional[Dict] = None,
        force_update: bool = False,
        context: Optional[Context] = None,
    ) -> None: ...

class EventOrigin(Enum):
    local: str
    remote: str

class EventBus:
    def async_fire(
        self,
        event_type: str,
        event_data: Optional[Dict] = None,
        origin: EventOrigin = EventOrigin.local,
        context: Optional[Context] = None,
    ) -> None: ...
    def async_listen_once(
        self, event_type: str, listener: Callable
    ) -> Callable[[], None]: ...
    def fire(
        self,
        event_type: str,
        event_data: Optional[Dict] = None,
        origin: EventOrigin = EventOrigin.local,
        context: Optional[Context] = None,
    ) -> None: ...

class ServiceRegistry:
    def async_register(
        self,
        domain: str,
        service: str,
        service_func: Callable,
        schema: Optional[vol.Schema] = None,
    ) -> None: ...

class Config:
    components: Set[str]

class AsyncGetRegistry(Protocol):
    def __call__(
        self, hass: Optional[HomeAssistant] = None
    ) -> Awaitable[DeviceRegistry]: ...

class DeviceRegistryModule(NamedTuple):
    async_get_registry: AsyncGetRegistry

class Helpers:
    device_registry: DeviceRegistryModule

class HomeAssistant:
    bus: EventBus
    config: Config
    config_entries: ConfigEntries
    data: dict
    helpers: Helpers
    services: ServiceRegistry
    states: StateMachine
    def async_create_task(self, target: Coroutine) -> asyncio.tasks.Task: ...

class ServiceCall:
    data: Dict

class Event: ...
