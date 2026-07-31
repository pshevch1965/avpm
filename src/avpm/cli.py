"""
AVPM command line interface.
"""

from avpm import __app_name__, __version__


def main() -> None:
    print(f"{__app_name__}")
    print("AdGuard VPN Manager")
    print()
    print(f"Version: {__version__}")