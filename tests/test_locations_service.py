from __future__ import annotations

import unittest

from avpm.models import Location
from avpm.services.locations import (
    fastest_location,
    filter_locations,
    search_locations,
    sort_by_ping,
)


class FilterLocationsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.locations = [
            Location("DE", "Germany", "Berlin", 42),
            Location("DE", "Germany", "Frankfurt", 57),
            Location("EE", "Estonia", "Tallinn", 18),
            Location("XX", "Unknown", "Unknown", None),
        ]

    def test_filters_by_iso_case_insensitively(self) -> None:
        result = filter_locations(self.locations, country="de")

        self.assertEqual(
            [location.city for location in result],
            ["Berlin", "Frankfurt"],
        )

    def test_filters_by_country_name_case_insensitively(self) -> None:
        result = filter_locations(self.locations, country="ESTONIA")

        self.assertEqual([location.city for location in result], ["Tallinn"])

    def test_filters_by_max_ping_and_excludes_unknown_ping(self) -> None:
        result = filter_locations(self.locations, max_ping=50)

        self.assertEqual(
            [location.city for location in result],
            ["Berlin", "Tallinn"],
        )

    def test_combines_country_and_max_ping(self) -> None:
        result = filter_locations(
            self.locations,
            country="DE",
            max_ping=50,
        )

        self.assertEqual([location.city for location in result], ["Berlin"])


class SearchLocationsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.locations = [
            Location("DE", "Germany", "Berlin", 42),
            Location("EE", "Estonia", "Tallinn", 18),
            Location("US", "United States", "New York", 120),
            Location("RO", "Romania", "Bucharest", 39),
            Location("HU", "Hungary", "Budapest", 42),
            Location("GB", "United Kingdom", "Manchester", 77),
        ]

    def test_searches_iso_country_and_city(self) -> None:
        self.assertEqual(
            [item.city for item in search_locations(self.locations, "EE")],
            ["Tallinn"],
        )
        self.assertEqual(
            [item.city for item in search_locations(self.locations, "united")],
            ["New York", "Manchester"],
        )
        self.assertEqual(
            [item.city for item in search_locations(self.locations, "berl")],
            ["Berlin"],
        )

    def test_search_is_case_insensitive(self) -> None:
        result = search_locations(self.locations, "TALL")

        self.assertEqual([item.city for item in result], ["Tallinn"])

    def test_returns_empty_list_without_matches(self) -> None:
        self.assertEqual(search_locations(self.locations, "missing"), [])

    def test_does_not_match_inside_words(self) -> None:
        result = search_locations(self.locations, "est")

        self.assertEqual([item.city for item in result], ["Tallinn"])

    def test_matches_beginning_of_later_word(self) -> None:
        result = search_locations(self.locations, "york")

        self.assertEqual([item.city for item in result], ["New York"])


class SortByPingTests(unittest.TestCase):
    def test_sorts_locations_by_ping(self) -> None:
        locations = [
            Location("DE", "Germany", "Berlin", 42),
            Location("LV", "Latvia", "Riga", 18),
            Location("SE", "Sweden", "Stockholm", 31),
        ]

        result = sort_by_ping(locations)

        self.assertEqual([location.iso for location in result], ["LV", "SE", "DE"])

    def test_places_unknown_ping_last(self) -> None:
        locations = [
            Location("XX", "Unknown", "Unknown", None),
            Location("UA", "Ukraine", "Kyiv", 20),
        ]

        result = sort_by_ping(locations)

        self.assertEqual([location.iso for location in result], ["UA", "XX"])

    def test_does_not_modify_input_list(self) -> None:
        locations = [
            Location("DE", "Germany", "Berlin", 42),
            Location("LV", "Latvia", "Riga", 18),
        ]

        sort_by_ping(locations)

        self.assertEqual([location.iso for location in locations], ["DE", "LV"])


class FastestLocationTests(unittest.TestCase):
    def test_returns_location_with_lowest_ping(self) -> None:
        locations = [
            Location("DE", "Germany", "Berlin", 42),
            Location("LV", "Latvia", "Riga", 18),
            Location("SE", "Sweden", "Stockholm", 31),
        ]

        result = fastest_location(locations)

        self.assertIsNotNone(result)
        self.assertEqual(result.city, "Riga")

    def test_ignores_locations_without_ping(self) -> None:
        locations = [
            Location("XX", "Unknown", "Unknown", None),
            Location("UA", "Ukraine", "Kyiv", 20),
        ]

        result = fastest_location(locations)

        self.assertIsNotNone(result)
        self.assertEqual(result.city, "Kyiv")

    def test_returns_none_without_known_ping(self) -> None:
        locations = [Location("XX", "Unknown", "Unknown", None)]

        self.assertIsNone(fastest_location(locations))


if __name__ == "__main__":
    unittest.main()
