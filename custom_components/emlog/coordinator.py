from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, EMLOG_EXPORT_PATH


_LOGGER = logging.getLogger(__name__)


@dataclass
class EmlogData:
    strom: dict
    gas: dict


class EmlogCoordinator(DataUpdateCoordinator[EmlogData]):
    def __init__(self, hass: HomeAssistant, host: str, strom_index: int, gas_index: int, scan_interval_s: int):
        self.hass = hass
        self.host = host
        self.strom_index = strom_index
        self.gas_index = gas_index

        super().__init__(
            hass,
            logger=_LOGGER,
            name=f"{DOMAIN}_{host}",
            update_interval=timedelta(seconds=scan_interval_s),
        )

    async def _fetch_export(self, meterindex: int) -> dict:
        session = async_get_clientsession(self.hass)
        url = f"http://{self.host}{EMLOG_EXPORT_PATH}?export&meterindex={meterindex}"

        try:
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    raise UpdateFailed(f"HTTP {resp.status} from {url}")
                return await resp.json(content_type=None)
        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Timeout while fetching {url}") from err
        except Exception as err:
            raise UpdateFailed(f"Error while fetching {url}: {err}") from err

    async def _async_update_data(self) -> EmlogData:
        strom = await self._fetch_export(self.strom_index)
        gas = await self._fetch_export(self.gas_index)
        return EmlogData(strom=strom, gas=gas)
