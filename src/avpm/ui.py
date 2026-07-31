"""
Output helpers.
"""

from __future__ import annotations


def title(version: str) -> None:
    print("=" * 42)
    print(f" AVPM {version}")
    print("=" * 42)


def info(text: str) -> None:
    print(text)


def error(text: str) -> None:
    print(f"ERROR: {text}")