from __future__ import annotations

import argparse
from argparse import Namespace

from avpm.models import Location


COMMANDS = {
    "version": "Show AVPM version",
    "about": "About AVPM",
    "help": "Show help",
    "status": "Show VPN status",
    "toggle": "Toggle VPN connection",
    "backend": "Show backend information",
    "on": "Connect VPN",
    "off": "Disconnect VPN",
    "locations": "List VPN locations",
    "doctor": "Run diagnostics",
    "connect": "Connect VPN",
    "disconnect": "Disconnect VPN",
    "reconnect": "Reconnect VPN",
    "fastest": "Show fastest VPN locations",
    "find": "Search VPN locations",
    "ip": "Show public IP address",
    "health": "Check VPN connection health",
    "support": "Create a diagnostic support archive",
    "watch": "Watch VPN connection status",
    "config": "Manage AVPM configuration",
    "completion": "Generate shell completion",
}

OPTIONS = {
    "status": ("-h", "--help", "-q", "--quiet", "--json"),
    "toggle": ("-h", "--help"),
    "on": ("-h", "--help", "-l", "--location"),
    "locations": (
        "-h",
        "--help",
        "-c",
        "--country",
        "--max-ping",
        "--json",
    ),
    "connect": ("-h", "--help", "-f", "--fastest", "-c", "--country"),
    "reconnect": (
        "-h",
        "--help",
        "-f",
        "--fastest",
        "-c",
        "--country",
        "--if-needed",
    ),
    "fastest": ("-h", "--help", "-c", "--country", "--json"),
    "find": ("-h", "--help", "--max-ping", "--json"),
    "ip": ("-h", "--help", "--json"),
    "health": ("-h", "--help", "--json"),
    "support": ("-h", "--help", "-o", "--output", "--include-logs"),
    "watch": ("-h", "--help", "-i", "--interval", "-n", "--count", "--json"),
    "config": (
        "-h",
        "--help",
        "--json",
        "show",
        "get",
        "set",
        "unset",
        "path",
        "default_country",
        "watch_interval",
        "output_format",
    ),
    "completion": ("-h", "--help", "bash", "zsh"),
}

OPTION_DESCRIPTIONS = {
    "-h": "Show help",
    "--help": "Show help",
    "-q": "Return connection state as exit code",
    "--quiet": "Return connection state as exit code",
    "--json": "Print JSON output",
    "-l": "Select VPN location",
    "--location": "Select VPN location",
    "-c": "Filter by country",
    "--country": "Filter by country",
    "--max-ping": "Set maximum ping",
    "-f": "Use fastest location",
    "--fastest": "Use fastest location",
    "--if-needed": "Connect only when disconnected",
    "-o": "Set output archive path",
    "--output": "Set output archive path",
    "--include-logs": "Include raw AdGuard VPN logs",
    "-i": "Set refresh interval",
    "--interval": "Set refresh interval",
    "-n": "Set update count",
    "--count": "Set update count",
    "bash": "Generate Bash completion",
    "zsh": "Generate Zsh completion",
}

ZSH_VALUE_ARGUMENTS = {
    "-l": ":location:->locations",
    "--location": ":location:->locations",
    "-c": ":country:->countries",
    "--country": ":country:->countries",
    "--max-ping": ":milliseconds:",
    "-o": ":file:_files",
    "--output": ":file:_files",
    "-i": ":seconds:",
    "--interval": ":seconds:",
    "-n": ":updates:",
    "--count": ":updates:",
}

ZSH_POSITIONAL_ARGUMENTS = {
    "connect": ("1:location:->locations",),
    "reconnect": ("1:location:->locations",),
    "fastest": ("1:count:",),
    "find": ("1:query:",),
    "completion": ("1:shell:(bash zsh)",),
    "config": (
        "1:action:(show get set unset path)",
        "2:key:(default_country watch_interval output_format)",
        "3:value:",
    ),
}


def completion_candidates(
    locations: list[Location],
    kind: str,
) -> list[str]:
    if kind == "countries":
        countries = {
            (location.iso, location.country)
            for location in locations
        }

        return [
            candidate
            for iso, country in sorted(countries)
            for candidate in (f"{iso}:{country}", f"{country}:{iso}")
        ]

    return sorted({
        f"{location.city}:{location.country} ({location.iso})"
        for location in locations
    })


def print_completion_candidates(kind: str) -> int:
    from avpm.backends.adguard import AdGuardBackend

    for candidate in completion_candidates(
        AdGuardBackend().locations(),
        kind,
    ):
        print(candidate)

    return 0


def bash_completion() -> str:
    commands = " ".join(("-h", "--help", *COMMANDS))
    cases = "\n".join(
        f"        {command}) options=\"{' '.join(options)}\" ;;"
        for command, options in OPTIONS.items()
    )

    return f"""\
_vpn_country_cache=()
_vpn_location_cache=()
_vpn_country_cache_time=-300
_vpn_location_cache_time=-300

_vpn_refresh_country_cache() {{
    if (( SECONDS - _vpn_country_cache_time < 300 && ${{#_vpn_country_cache[@]}} )); then
        return
    fi

    _vpn_country_cache=()
    local candidate

    while IFS= read -r candidate; do
        _vpn_country_cache+=("${{candidate%%:*}}")
    done < <(vpn completion bash --candidates countries 2>/dev/null)

    _vpn_country_cache_time=$SECONDS
}}

_vpn_refresh_location_cache() {{
    if (( SECONDS - _vpn_location_cache_time < 300 && ${{#_vpn_location_cache[@]}} )); then
        return
    fi

    _vpn_location_cache=()
    local candidate

    while IFS= read -r candidate; do
        _vpn_location_cache+=("${{candidate%%:*}}")
    done < <(vpn completion bash --candidates locations 2>/dev/null)

    _vpn_location_cache_time=$SECONDS
}}

_vpn_complete_values() {{
    local current="$1"
    shift
    local candidate

    COMPREPLY=()

    for candidate in "$@"; do
        if [[ $candidate == "$current"* ]]; then
            COMPREPLY+=("$candidate")
        fi
    done
}}

_vpn_completion() {{
    local command current options previous
    COMPREPLY=()
    current="${{COMP_WORDS[COMP_CWORD]}}"

    if [[ $COMP_CWORD -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "{commands}" -- "$current") )
        return 0
    fi

    command="${{COMP_WORDS[1]}}"
    previous="${{COMP_WORDS[COMP_CWORD - 1]}}"

    if [[ $previous == -c || $previous == --country ]]; then
        _vpn_refresh_country_cache
        _vpn_complete_values "$current" "${{_vpn_country_cache[@]}}"
        return 0
    fi

    if [[ $previous == -l || $previous == --location ]]; then
        _vpn_refresh_location_cache
        _vpn_complete_values "$current" "${{_vpn_location_cache[@]}}"
        return 0
    fi

    if [[ $previous == -o || $previous == --output ]]; then
        COMPREPLY=( $(compgen -f -- "$current") )
        return 0
    fi

    if [[ $COMP_CWORD -eq 2 && ($command == connect || $command == reconnect) && $current != -* ]]; then
        _vpn_refresh_location_cache
        _vpn_complete_values "$current" "${{_vpn_location_cache[@]}}"
        return 0
    fi

    case "$command" in
{cases}
        *) options="-h --help" ;;
    esac

    COMPREPLY=( $(compgen -W "$options" -- "$current") )
}}

complete -F _vpn_completion vpn
"""


def zsh_completion() -> str:
    commands = "\n".join(
        f"        '{command}:{description}'"
        for command, description in COMMANDS.items()
    )
    cases = []

    for command, options in OPTIONS.items():
        specs = [
            f"{option}[{OPTION_DESCRIPTIONS[option]}]"
            f"{ZSH_VALUE_ARGUMENTS.get(option, '')}"
            for option in options
            if option.startswith("-")
        ]
        positional = ZSH_POSITIONAL_ARGUMENTS.get(command)

        if positional:
            specs.extend(positional)

        arguments = " ".join(repr(spec) for spec in specs)
        cases.append(f"        {command}) _arguments {arguments} ;;")

    cases_text = "\n".join(cases)

    return f"""\
#compdef vpn

typeset -ga _vpn_country_cache _vpn_location_cache
typeset -gi _vpn_country_cache_time=-300
typeset -gi _vpn_location_cache_time=-300

_vpn_complete_countries() {{
    if (( SECONDS - _vpn_country_cache_time >= 300 || !$#_vpn_country_cache )); then
        _vpn_country_cache=("${{(@f)$(vpn completion zsh --candidates countries 2>/dev/null)}}")
        _vpn_country_cache_time=$SECONDS
    fi

    _describe 'country' _vpn_country_cache
}}

_vpn_complete_locations() {{
    if (( SECONDS - _vpn_location_cache_time >= 300 || !$#_vpn_location_cache )); then
        _vpn_location_cache=("${{(@f)$(vpn completion zsh --candidates locations 2>/dev/null)}}")
        _vpn_location_cache_time=$SECONDS
    fi

    _describe 'location' _vpn_location_cache
}}

_vpn() {{
    local -a commands
    local context state state_descr line
    typeset -A opt_args

    commands=(
{commands}
    )

    if (( CURRENT == 2 )); then
        _describe 'command' commands
        return
    fi

    local command="$words[2]"
    words=("${{words[@]:1}}")
    (( CURRENT-- ))

    case "$command" in
{cases_text}
        *) _arguments '-h[Show help]' '--help[Show help]' ;;
    esac

    case "$state" in
        countries) _vpn_complete_countries ;;
        locations) _vpn_complete_locations ;;
    esac
}}

compdef _vpn vpn
"""


def run(args: Namespace) -> int:
    candidates = getattr(args, "candidates", None)

    if candidates:
        return print_completion_candidates(candidates)

    script = bash_completion() if args.shell == "bash" else zsh_completion()
    print(script, end="")
    return 0


def register(subparsers) -> None:
    parser = subparsers.add_parser(
        "completion",
        help="Generate shell completion",
    )

    parser.add_argument(
        "shell",
        choices=("bash", "zsh"),
        help="Shell syntax to generate",
    )

    parser.add_argument(
        "--candidates",
        choices=("countries", "locations"),
        help=argparse.SUPPRESS,
    )

    parser.set_defaults(func=run)
