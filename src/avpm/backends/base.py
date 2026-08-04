from abc import ABC, abstractmethod

from avpm.models import Location, VPNStatus


class Backend(ABC):

    @abstractmethod
    def exists(self) -> bool:
        ...

    @abstractmethod
    def status(self) -> VPNStatus:
        ...

    @abstractmethod
    def connect(self, location: str | None = None) -> str:
        ...

    @abstractmethod
    def disconnect(self) -> None:
        ...

    @abstractmethod
    def locations(self) -> list[Location]:
        """Return available VPN locations."""

