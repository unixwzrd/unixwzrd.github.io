---
layout: post
title:  "Dark Mode Test Post"
date:   2024-08-15 23:45:00 -0500
categories: test
excerpt: "This is a paragraph with some **bold text** and _italic text_. Here's a link."
---
image: /assets/images/default-og-image.png

## Just a test page here, testing formats

<!--more-->

# Heading Level 1
## Heading Level 2
### Heading Level 3
#### Heading Level 4
##### Heading Level 5
###### Heading Level 6

This is a paragraph with some **bold text** and _italic text_. Here's a [link](https://example.com).

> This is a blockquote. It's often used to highlight text.

### Lists

- Unordered list item 1
- Unordered list item 2
  - Nested item
- Unordered list item 3

1. Ordered list item 1
2. Ordered list item 2
   1. Nested ordered item
3. Ordered list item 3

### Table

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Row 1    | Data 1   | Data 2   |
| Row 2    | Data 3   | Data 4   |

### Inline Code

Here's some inline code: `print("Hello, world!")`

### Code Block

```python
import os
from datetime import datetime
import json
from typing import List, Optional
import yaml
from pydantic import Field
from modules.Turn import Turn
from modules.User import User
from modules.AppConfig import AppConfig
from modules.Actor import Actor
from modules.HyperParameters import HyperParameters
from modules.SymbolConverter import SymbolConverter
from modules.Utils import FileUtils
from modules.BaseSerializable import BaseSerializable

class Conversation(BaseSerializable):
    app_config = AppConfig()
    name: str = ""
    start_time: str = Field(default_factory=lambda: datetime.now().isoformat())
    update_time: str = Field(default_factory=lambda: datetime.now().isoformat())
    user: Optional[User] = None
    actor: Optional[Actor] = None
    current_model: str = ""
    current_hyperparameters: HyperParameters = Field(default_factory=HyperParameters)
    turns: List[Turn] = Field(default_factory=list)

    def add_turn(self, message: str, role: str, model_name: Optional[str] = None, token_count: Optional[int] = None):
        new_turn = Turn(
            message=message,
            role=role,
            model_name=model_name,
            token_count=token_count
        )
        if self.turns:
            self.turns[-1].add_child(new_turn)
            new_turn.parent_id = self.turns[-1].id
        self.turns.append(new_turn)

    def load_from_file(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            if "internal" in data and "visible" in data:
                self.load_legacy_format(data, filename)
            else:
                self.type = data.get('type', 'actor_conversation')
                self.version = data.get('version', 1.0)
                self.name = data['name']
                self.filename = data['filename']
                self.start_time = data['start_time']
                self.update_time = data['update_time']
                self.turns = [Turn.from_dict(turn_data) for turn_data in data['turns']]
                if data.get('user'):
                    self.user = User(**data['user'])
                if data.get('actor'):
                    self.actor = Actor(**data['actor'])
                self.update_current_settings()
```

```bash
do_wrapper() {
#
# do_wrapper - General wrapper function for logging specific command actions
#
# - **Purpose**:
#   - Executes a Python package maneger command with optional logging based on the specified action.
# - **Usage**:
#   - `do_wrapper <cmd> <additional parameters>`
#  - **Parameters**:
#    - cmd: The command to be executed.
#    - Additional parameters: Any additional parameters to be passed to the command.
# - **Returns**:
#   - None
#
    local cmd="$1"; shift
    local action="$1"
    local actions_to_log=("install" "uninstall" "remove" "rename" "update" "upgrade" "create" "clean" "config" "clone")
    local actions_to_exclude=("--help" "-h" "--dry-run")
    local cmd_args="$@"
    local env_vars
    env_vars=$( env | sed -E '/^SHELL=/,$d' | sed -E 's/^([A-Za-z_]+)=(.*)$/\1="\2"/' | tr '\n' ' ' )

    # Make the command be how the user invoked it rather than with the wrappers.
    local user_cmd=$(echo "${cmd} ${cmd_args}" | sed 's/__venv_//g')

    # Check if the command ${cmd} is a file or a function/alias. If it's not a function,
    # we want to run it with the "command" builtin to bypass shell functions or aliases.
    if type -P ${cmd} &>/dev/null; then
        cmd="command ${cmd}"
    fi

    # local cmd_line="${env_vars} ${cmd} ${cmd_args}"
    local user_line="${env_vars} ${user_cmd} ${cmd_args}"

    # Check if the action is potentially destructive and should be logged.
    if [[ " ${actions_to_log[*]} " =~ "${action}" ]] && ! [[ "$*" =~ $(IFS="|"; echo "${actions_to_exclude[*]}") ]]; then
        local file_date=$(date "+%Y%m%d%H%M%S")
        local cmd_date=$(date '+%Y-%m-%d %H:%M:%S')
        local freeze_dir="${VENVUTIL_CONFIG}/freeze"
        local freeze_state="${freeze_dir}/${CONDA_DEFAULT_ENV}.${file_date}.txt"
        # Freeze the state of the environment before a potentially destructive command is executed.
        command pip freeze > "${freeze_state}"
        if eval " ${env_vars} ${cmd} ${cmd_args} "; then
            local hist_log="${VENVUTIL_CONFIG}/${CONDA_DEFAULT_ENV}.log"
            # Logging the command invocation if it completed successfully.
            echo "# ${cmd_date}: ${user_line}" >> "${hist_log}"
            echo "# ${cmd_date}: $(${cmd} --version)" >> "${hist_log}"
            local venvutil_log="${VENVUTIL_CONFIG}/venvutil.log"
            echo "# ${cmd_date} - ${CONDA_DEFAULT_ENV}: ${user_line}" >> "${venvutil_log}"
        fi
    else
        # Execute the command without logging.
        ${cmd} ${cmd_args}
    fi
}
```

### Image

![Test Image](https://via.placeholder.com/150)
