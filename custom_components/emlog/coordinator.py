from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, EMLOG_EXPORT_PATH

_LOGGER = logging.getLogger(__name__)


@dataclass
class EmlogData:
    """Data from Emlog API for a single meter."""

    meter_data: dict  # Raw JSON data from API
    api_status: str = "connected"  # "connected" oder "failed" oder "initializing"
    last_error: str | None = None  # Fehlerbeschreibung bei Fehler
    last_successful_update: datetime | None = None  # Letzter erfolgreicher Update
    currency: str = "EUR"  # Währung aus API, default EUR


class EmlogCoordinator(DataUpdateCoordinator[EmlogData]):
    """Coordinator für einen einzelnen Emlog-Zähler (Strom ODER Gas)."""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        meter_type: str,
        meter_index: int,
        scan_interval_s: int,
        config_entry=None,
    ):
        self.hass = hass
        self.host = host
        self.meter_type = meter_type  # "strom" oder "gas"
        self.meter_index = meter_index
        self.config_entry = config_entry  # Store for dynamic value access
        self._failed_updates = 0  # Zähler für aufeinanderfolgende Fehler
        self._last_error: str | None = None  # Beschreibung des letzten Fehlers

        super().__init__(
            hass,
            logger=_LOGGER,
            name=f"{DOMAIN}_{host}_{meter_type}_{meter_index}",
            update_interval=timedelta(seconds=scan_interval_s),
        )

    async def _fetch_export(self) -> tuple[dict | None, str | None]:
        """Fetch export data from Emlog.

        Returns:
            Tuple of (data, error_message)
            - (dict, None): Erfolgreich
            - (None, str): Fehler
        """
        session = async_get_clientsession(self.hass)
        url = f"http://{self.host}{EMLOG_EXPORT_PATH}?export&meterindex={self.meter_index}"

        try:
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    error_msg = f"HTTP {resp.status} von {self.host} (Index {self.meter_index})"
                    _LOGGER.warning(error_msg)
                    return None, error_msg
                return await resp.json(content_type=None), None
        except asyncio.TimeoutError:
            error_msg = f"Timeout beim Verbindungsaufbau zu {self.host} (Index {self.meter_index})"
            _LOGGER.warning(error_msg)
            return None, error_msg
        except Exception as err:
            error_msg = f"Fehler bei {self.host} (Index {self.meter_index}): {type(err).__name__} - {err}"
            _LOGGER.warning(error_msg)
            return None, error_msg

    async def _async_update_data(self) -> EmlogData:
        """Fetch data from API.

        Home Assistant Best Practice:
        - Bei temporären Fehlern: Alte Daten beibehalten
        - Entities bleiben 'available' solange möglich
        - UpdateFailed Exception NICHT werfen (graceful degradation)
        - Bei API-Fehlern: status="failed" mit Fehlerdetails zurückgeben

        Verhalten:
        - API erreichbar: Neue Daten, api_status="connected", last_error=None
        - API nicht erreichbar: Alte Daten behalten, api_status="failed", last_error=Details
        - Keine alten Daten: Leere Daten mit failed status
        """
        meter_data, error = await self._fetch_export()

        if error:
            # Fehler beim Abrufen der Daten
            self._failed_updates += 1
            self._last_error = error

            # Kürze Fehlermeldung auf 200 Zeichen (HA State Limit: 255)
            last_error = error
            if len(last_error) > 200:
                last_error = last_error[:197] + "..."

            # Gib alte Daten zurück wenn vorhanden
            if self.data is not None:
                _LOGGER.info(
                    f"API temporarily unavailable - keeping last known values "
                    f"(failed updates: {self._failed_updates})"
                )
                return EmlogData(
                    meter_data=self.data.meter_data,
                    api_status="failed",
                    last_error=last_error,
                    last_successful_update=self.data.last_successful_update,
                    currency=self.data.currency,
                )

            # Beim allerersten Fehler: Gib fehlerhafte Daten zurück
            _LOGGER.debug("No previous data available, returning empty data with failed status")
            return EmlogData(
                meter_data={},
                api_status="failed",
                last_error=last_error,
                last_successful_update=None,
                currency="EUR",
            )

        # Erfolgreicher Update - Reset counter
        if self._failed_updates > 0:
            _LOGGER.info(f"Connection to Emlog API restored after {self._failed_updates} failed attempts")
        self._failed_updates = 0
        self._last_error = None

        # Nutze HA Timezone falls verfügbar, sonst UTC
        if hasattr(self.hass, "config") and self.hass.config.time_zone:
            from homeassistant.util import dt as dt_util

            tz = dt_util.get_time_zone(self.hass.config.time_zone)
            now = datetime.now(tz) if tz else datetime.now(timezone.utc)
        else:
            now = datetime.now(timezone.utc)

        # Extrahiere Währung aus API-Response
        currency = "EUR"  # Default
        if meter_data:
            # Versuche Währung aus verschiedenen Positionen zu extrahieren
            currency = (
                meter_data.get("Betrag_Bezug", {}).get("Waehrung")
                or meter_data.get("Betrag_Lieferung", {}).get("Waehrung")
                or "EUR"
            )

        return EmlogData(
            meter_data=meter_data or {},
            api_status="connected",
            last_error=None,
            last_successful_update=now,
            currency=currency,
        )
