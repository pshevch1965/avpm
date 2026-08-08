# Changelog

## 0.3.0-alpha3

Added:

- `connect --fastest` and country-scoped fastest connections
- `reconnect --if-needed`, `--fastest`, and combined modes
- country and maximum-ping filters for `locations`
- country filtering for `fastest`
- quiet status mode with script-friendly exit codes
- service modules for locations, connection selection, and status parsing
- unit tests for commands, services, and the AdGuard backend

Fixed:

- disconnected status was incorrectly detected as connected
- `vpn help` displayed an empty parser instead of root help
- fastest-location selection requested the location list twice
- locations with unknown ping could break sorting
- missing backend checks and command error imports

Changed:

- shared fastest-location logic is used by `connect` and `reconnect`
- CLI output and location-table formatting are centralized

## 0.2.0-alpha2

Initial project bootstrap.

Added:

- project structure
- Python package layout
- documentation skeleton
- driver architecture foundation
