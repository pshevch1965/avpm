# AVPM

[![CI](https://github.com/pshevch1965/avpm/actions/workflows/ci.yml/badge.svg?branch=develop)](https://github.com/pshevch1965/avpm/actions/workflows/ci.yml)

AVPM (AdGuard VPN Manager) is a Python command-line manager for
`adguardvpn-cli` on Linux.

Current version: **0.4.0-alpha4**

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
| `vpn status --json` | Show structured connection status |
| `vpn toggle` | Connect when disconnected, or disconnect when connected |
| `vpn locations` | List VPN locations |
| `vpn find QUERY` | Search locations by ISO code, country, or city |
| `vpn ip` | Show the current public IPv4 or IPv6 address |
| `vpn health` | Check VPN state, tunnel interface, and public IP |
| `vpn support` | Create a privacy-conscious diagnostic archive |
| `vpn watch` | Monitor VPN status continuously |
| `vpn config` | Manage persistent AVPM settings |
| `vpn fastest [count]` | Show the locations with the lowest ping |
| `vpn connect [location]` | Connect to the last or specified location |
| `vpn disconnect` | Disconnect the VPN |
| `vpn reconnect [location]` | Reconnect to the last or specified location |
| `vpn doctor` | Check Python, system, and AdGuard CLI availability |
| `vpn help` | Show the complete command list |
| `vpn completion bash|zsh` | Generate shell completion |

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

Search across ISO codes, country names, and city names:

```bash
vpn find est
vpn find berlin
vpn find united --max-ping 200
vpn find tallinn --json
```

Show the public IP address observed outside the VPN tunnel:

```bash
vpn ip
vpn ip --json
```

Check the complete connection health and use the exit code in scripts:

```bash
vpn health
vpn health --json
vpn health >/dev/null || echo "VPN health check failed"
```

Create a diagnostic archive for troubleshooting:

```bash
vpn support
vpn support --output ~/Downloads/avpm-support.zip
```

The default archive excludes the public IP address, username, home path,
environment variables, and raw logs. Add raw AdGuard VPN logs only when they
are needed, and review the archive before sharing it:

```bash
vpn support --include-logs
```

Watch the VPN state until `Ctrl+C`, or limit the number of updates:

```bash
vpn watch
vpn watch --interval 1 --count 10
vpn watch --count 3 --json
```

Manage persistent configuration stored under the XDG config directory:

```bash
vpn config show
vpn config set default_country EE
vpn config set watch_interval 1.5
vpn config set output_format json
vpn config get default_country
vpn config unset default_country
vpn config path
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

Structured output is available for integrations and future GUI clients:

```bash
vpn status --json
vpn locations --json
vpn locations --country DE --json
vpn fastest 5 --json
```

`status --quiet` and `status --json` are mutually exclusive.

## Shell completion

Enable completion for the current Bash session:

```bash
source <(vpn completion bash)
```

Install Bash completion permanently:

```bash
mkdir -p ~/.local/share/bash-completion/completions
vpn completion bash > ~/.local/share/bash-completion/completions/vpn
```

Enable completion for the current Zsh session:

```zsh
source <(vpn completion zsh)
```

Install Zsh completion permanently:

```zsh
mkdir -p ~/.local/share/zsh/site-functions
vpn completion zsh > ~/.local/share/zsh/site-functions/_vpn
fpath=(~/.local/share/zsh/site-functions $fpath)
autoload -Uz compinit && compinit
```

Bash and Zsh also complete country names, ISO codes, and VPN cities. Location
data is cached for five minutes in the current shell session to avoid repeated
ping measurements on every completion request.

## Tests

Install the project in editable mode, then run the complete test suite:

```bash
python -m unittest discover -s tests -v
```

The tests do not require an active AdGuard VPN connection.

## License

MIT
