#!/usr/bin/env bash
# Source only: select existing local project environments without installing
# packages, changing defaults, or affecting the caller's parent shell.
site_environment() {
    local ruby_environment="${HOME}/.rvm/environments/ext-ruby-3.3.4@unixwzrd.github.io"
    local conda_root conda_prefix
    if [ -f "$ruby_environment" ]; then
        source "$ruby_environment" || return
    fi
    for conda_root in "${HOME}/miniconda3" "${HOME}/anaconda3"; do
        conda_prefix="${conda_root}/envs/python-website-dev"
        if [ -x "${conda_prefix}/bin/python" ]; then
            if [ ! -f "${conda_root}/etc/profile.d/conda.sh" ]; then
                echo "Conda activation script missing for ${conda_prefix}" >&2
                return 1
            fi
            source "${conda_root}/etc/profile.d/conda.sh" || return
            conda activate "$conda_prefix" || return
            break
        fi
    done
    hash -r
}

