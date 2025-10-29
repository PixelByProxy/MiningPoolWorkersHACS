"""Base entity for the Miner Pool Stats integration."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, WALLET_ADDRESS, WORKER, CryptoCoin
from .coordinator import PoolConfigEntry, PoolCoordinator
from .pool import PoolInitData


class PoolAddressDeviceEntity(CoordinatorEntity[PoolCoordinator]):
    """Representation of a Pool Address base entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PoolCoordinator,
        config_entry: PoolConfigEntry,
        pool_config: PoolInitData,
    ) -> None:
        """Initialize base entity."""
        super().__init__(coordinator)
        try:
            coin = CryptoCoin(pool_config.coin_key).name
        except ValueError:
            coin = pool_config.coin_key
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, config_entry.entry_id)},
            manufacturer=pool_config.pool_name,
            model=f"{coin} {WALLET_ADDRESS}",
            name=pool_config.address,
        )


class PoolAddressWorkerDeviceEntity(CoordinatorEntity[PoolCoordinator]):
    """Representation of a Pool Address Worker base entity."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PoolCoordinator,
        config_entry: PoolConfigEntry,
        pool_config: PoolInitData,
        worker_name: str,
    ) -> None:
        """Initialize base entity."""
        super().__init__(coordinator)
        try:
            coin = CryptoCoin(pool_config.coin_key).name
        except ValueError:
            coin = pool_config.coin_key
        self.worker_name = worker_name
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{config_entry.entry_id}-{worker_name}")},
            manufacturer=pool_config.pool_name,
            model=f"{coin} {WORKER}",
            name=worker_name,
        )
