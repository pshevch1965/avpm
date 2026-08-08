# AVPM

AVPM (AdGuard VPN Manager) is a Python command-line manager for
`adguardvpn-cli` on Linux.

Current version: **0.3.0-alpha3**

## Requirements

- Linux
- Python 3.10 or newer
- `adguardvpn-cli` 1.7 or newer
- an authenticated AdGuard VPN CLI session

## Installation for development

```bash
git clone https://github.com/pshevch1965/avpm.git
cd avpm
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Verify the installation:

```bash
vpn version
vpn doctor
```

## Commands

| Command | Purpose |
| --- | --- |
| `vpn status` | Show the raw AdGuard VPN connection status |
| `vpn status --quiet` | Return `0` when connected and `1` otherwise, without output |
| `vpn locations` | List VPN locations |
| `vpn fastest [count]` | Show the locations with the lowest ping |
| `vpn connect [location]` | Connect to the last or specified location |
| `vpn disconnect` | Disconnect the VPN |
| `vpn reconnect [location]` | Reconnect to the last or specified location |
| `vpn doctor` | Check Python, system, and AdGuard CLI availability |
| `vpn help` | Show the complete command list |

The shorter `vpn on` and `vpn off` aliases are also available.

## Location filters

Filter by ISO code or country name, by maximum ping, or by both:

```bash
vpn locations --country EE
vpn locations --country Estonia
vpn locations --max-ping 50
vpn locations --country DE --max-ping 60
```

Show the fastest locations inside one country:

```bash
vpn fastest 5 --country DE
```

## Fastest connection

Connect to the globally fastest location:

```bash
vpn connect --fastest
```

Limit selection to a country:

```bash
vpn connect --fastest --country DE
vpn reconnect --fastest --country EE
```

Avoid interrupting an already active connection:

```bash
vpn reconnect --if-needed
vpn reconnect --if-needed --fastest
vpn reconnect --if-needed --fastest --country EE
```

## Scripting

`status --quiet` exposes the connection state as an exit code:

```bash
vpn status --quiet || vpn reconnect --if-needed
```

## Tests

Install the project in editable mode, then run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

The tests do not require an active AdGuard VPN connection.

## License

MIT
