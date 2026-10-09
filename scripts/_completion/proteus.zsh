#compdef proteus proteus-backup proteus-calendar proteus-contacts proteus-cookbook proteus-docs proteus-gallery proteus-mail proteus-mcp proteus-memory proteus-notes proteus-personal proteus-preset proteus-research proteus-sessions proteus-signature proteus-skills proteus-tasks proteus-theme proteus-webhook
# Zsh tab-completion for the proteus umbrella + sub-CLIs.
#
# Drop in any directory on $fpath, e.g.:
#     fpath=(/path/to/proteus-ui/scripts/_completion $fpath)
#     autoload -U compinit; compinit
#
# Then `proteus <tab>` completes subcommands; `proteus mail <tab>`
# completes mail subcommands; `proteus-mail <tab>` works the same.

_proteus_scripts_dir() {
    local self="${(%):-%x}"
    while [[ -L "$self" ]]; do self="$(readlink "$self")"; done
    cd "${self:h}/.." && pwd
}

typeset -gA _proteus_subs

_proteus_refresh() {
    _proteus_subs=()
    local dir="$(_proteus_scripts_dir)"
    local py="$dir/../venv/bin/python"
    [[ -x "$py" ]] || py="$(command -v python3)"
    local f sub help_out commands
    for f in "$dir"/proteus-*; do
        [[ -x "$f" ]] || continue
        case "$f" in
            *.bak|*.pyc|*.pre-*) continue ;;
        esac
        sub="${${f:t}#proteus-}"
        help_out=$("$py" "$f" --help 2>/dev/null) || continue
        commands=$(echo "$help_out" | grep -oE '\{[a-z0-9_,-]+\}' | head -1 \
            | tr -d '{}' | tr ',' ' ')
        _proteus_subs[$sub]="$commands"
    done
}

_proteus() {
    [[ ${#_proteus_subs} -eq 0 ]] && _proteus_refresh

    local cmd="${words[1]}"

    if [[ "$cmd" == "proteus" ]]; then
        if (( CURRENT == 2 )); then
            local -a subs=(${(k)_proteus_subs} help)
            _describe 'subcommand' subs
            return
        fi
        local sub="${words[2]}"
        if [[ "$sub" == "help" ]] && (( CURRENT == 3 )); then
            local -a subs=(${(k)_proteus_subs})
            _describe 'subcommand' subs
            return
        fi
        if (( CURRENT == 3 )); then
            local -a sc=(${(s/ /)_proteus_subs[$sub]})
            _describe 'command' sc
            return
        fi
        return
    fi

    # proteus-foo <tab>
    local sub="${cmd#proteus-}"
    if (( CURRENT == 2 )); then
        local -a sc=(${(s/ /)_proteus_subs[$sub]})
        _describe 'command' sc
        return
    fi
}

_proteus "$@"
