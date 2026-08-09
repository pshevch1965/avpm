from __future__ import annotations

import unittest

from avpm.backends.adguard import AdGuardBackend
from avpm.backends.base import Backend


class BackendContractTests(unittest.TestCase):
    def test_adguard_backend_implements_canonical_contract(self) -> None:
        self.assertTrue(issubclass(AdGuardBackend, Backend))


if __name__ == "__main__":
    unittest.main()
