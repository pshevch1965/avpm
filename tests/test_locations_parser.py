from __future__ import annotations

import unittest

from avpm.services.locations import parse_locations


REAL_LOCATION_OUTPUT = """\
\x1b[1mISO   COUNTRY              CITY                           PING ESTIMATE
\x1b[0mEE    Estonia              Tallinn                        21
US    United States        Silicon Valley                 277
RU    Russia               Moscow (Virtual)               43
BR    Brazil               São Paulo                      342
MD    Moldova              Chișinău                       35
XX    Unknown              Test                           -
not a location

You can connect to a location by running `adguardvpn-cli connect -l 'city'`
"""


class ParseLocationsTests(unittest.TestCase):
    def test_parses_real_fixed_width_output(self) -> None:
        locations = parse_locations(REAL_LOCATION_OUTPUT)

        self.assertEqual(len(locations), 6)
        self.assertEqual(locations[0].iso, "EE")
        self.assertEqual(locations[0].city, "Tallinn")
        self.assertEqual(locations[0].ping, 21)

    def test_preserves_multi_word_values(self) -> None:
        locations = parse_locations(REAL_LOCATION_OUTPUT)

        silicon_valley = locations[1]
        self.assertEqual(silicon_valley.country, "United States")
        self.assertEqual(silicon_valley.city, "Silicon Valley")

        self.assertEqual(locations[2].city, "Moscow (Virtual)")

    def test_preserves_unicode_names(self) -> None:
        locations = parse_locations(REAL_LOCATION_OUTPUT)

        self.assertEqual(locations[3].city, "São Paulo")
        self.assertEqual(locations[4].city, "Chișinău")

    def test_uses_none_for_unknown_ping(self) -> None:
        locations = parse_locations(REAL_LOCATION_OUTPUT)

        self.assertIsNone(locations[5].ping)

    def test_ignores_malformed_and_footer_lines(self) -> None:
        locations = parse_locations(
            "garbage\nYou can connect to a location\nEE    ignored"
        )

        self.assertEqual(locations, [])


if __name__ == "__main__":
    unittest.main()
