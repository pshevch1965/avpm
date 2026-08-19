from __future__ import annotations


class AvpmError(Exception):
    """Base AVPM exception."""


class BackendError(AvpmError):
    """Backend execution error."""


class BackendNotFoundError(BackendError):
    """Backend executable not found."""


class NetworkError(AvpmError):
    """Network request failed."""
