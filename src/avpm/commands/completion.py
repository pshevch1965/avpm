from __future__ import annotations

from argparse import Namespace


COMMANDS = {
    "version": "Show AVPM version",
    "about": "About AVPM",
    "help": "Show help",
    "status": "Show VPN status",
    "backend": "Show backend information",
    "on": "Connect VPN",
    "off": "Disconnect VPN",
    "locations": "List VPN locations",
    "doctor": "Run diagnostics",
    "connect": "Connect VPN",
    "disconnect": "Disconnect VPN",
    "reconnect": "Reconnect VPN",
    "fastest": "Show fastest VPN locations",
    "completion": "Generate shell completion",
}

OPTIONS = {
    "status": ("-h", "--help", "-q", "--quiet", "--json"),
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
    "bash": "Generate Bash completion",
    "zsh": "Generate Zsh completion",
}

ZSH_VALUE_ARGUMENTS = {
    "-l": ":location:",
    "--location": ":location:",
    "-c": ":country:",
    "--country": ":country:",
    "--max-ping": ":milliseconds:",
}

ZSH_POSITIONAL_ARGUMENTS = {
    "connect": "1:location:",
    "reconnect": "1:location:",
    "fastest": "1:count:",
    "completion": "1:shell:(bash zsh)",
}


def bash_completion() -> str:
    commands = " ".join(("-h", "--help", *COMMANDS))
    cases = "\n".join(
        f"        {command}) options=\"{' '.join(options)}\" ;;"
        for command, options in OPTIONS.items()
    )

    return f"""\
_vpn_completion() {{
    local current options
    COMPREPLY=()
    current="${{COMP_WORDS[COMP_CWORD]}}"

    if [[ $COMP_CWORD -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "{commands}" -- "$current") )
        return 0
    fi

    case "${{COMP_WORDS[1]}}" in
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
            specs.append(positional)

        arguments = " ".join(repr(spec) for spec in specs)
        cases.append(f"        {command}) _arguments {arguments} ;;")

    cases_text = "\n".join(cases)

    return f"""\
#compdef vpn

_vpn() {{
    local -a commands

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
}}

compdef _vpn vpn
"""


def run(args: Namespace) -> int:
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

    parser.set_defaults(func=run)
