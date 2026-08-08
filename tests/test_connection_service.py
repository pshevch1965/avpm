from __future__ import annotations

import unittest
from unittest.mock import Mock

from avpm.exceptions import BackendError
from avpm.models import Location
from avpm.services.connection import get_fastest_location


class GetFastestLocationTests(unittest.TestCase):
    def test_returns_fastest_backend_location(self) -> None:
        backend = Mock()
        backend.locations.return_value = [
            Location("DE", "Germany", "Berlin", 42),
            Location("EE", "Estonia", "Tallinn", 17),
        ]

        result = get_fastest_location(backend)

        self.assertEqual(result.city, "Tallinn")
        backend.locations.assert_called_once_with()

    def test_raises_when_no_ping_is_available(self) -> None:
        backend = Mock()
        backend.locations.return_value = [
            Location("XX", "Unknown", "Unknown", None),
        ]

        with self.assertRaisesRegex(
            BackendError,
            "No VPN locations with known ping found",
        ):
            get_fastest_location(backend)

    def test_limits_selection_to_country(self) -> None:
        backend = Mock()
        backend.locations.return_value = [
            Location("DE", "Germany", "Berlin", 42),
            Location("EE", "Estonia", "Tallinn", 17),
        ]

        result = get_fastest_location(backend, country="DE")

        self.assertEqual(result.city, "Berlin")


if __name__ == "__main__":
    unittest.main()
