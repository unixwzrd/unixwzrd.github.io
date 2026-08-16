---
short_url: "https://unixwzrd.ai/s/c474212fd8/"
excerpt: "Use SSH host aliases, isolated user accounts, and secure tunnels to edit and debug Python on the same Mac or a remote system with VS Code, Cursor, Windsurf, and related editors."
image: /assets/images/vibing-remote-debugging.png
layout: post
title: "Remote Debugging with VS Code and Its Derivatives"
redirect_from:
  - /2025/04/08/Remote-Debugging-With-VSCode/
date: 2025-04-08 17:30:00 -0500
last_modified_at: 2026-08-15 20:30:00 -0500
update_notice_title: "Updated August 2026"
update_notice: "I rewrote this article around SSH key authentication, reusable host aliases, and development under a separate operating-system account. It now covers both another user on the same Mac and a remote machine, explains how VS Code-style remote workspaces differ from attaching to an existing process, and keeps the Python debugger behind an SSH tunnel instead of exposing it to the network."
categories: [technology]
tags: [debugging, vscode, cursor, windsurf, ssh, remote-development, python, developer-tools]
---

When I first wrote this article, I concentrated on the last few feet of the problem: start `debugpy`, forward a port, and attach the editor. That works, but it skips the part that determines whether the arrangement will remain useful after the first experiment. Before I can trust remote editing or debugging, I need a repeatable identity, a predictable SSH destination, and some separation between the environment where I write code and the environment where I run it.

That separation does not require another physical computer. A second account on the same Mac is enough to give the code a different home directory, shell environment, package configuration, editor server, and set of user-level services. When I do have another Mac or Linux system available, the workflow barely changes. I connect through a short alias from `~/.ssh/config`, and the editor uses the same OpenSSH configuration that already works in my terminal.

If you want to build the complete arrangement rather than read about its parts, the companion tutorial [Hands-On: Isolated Remote Development with SSH](/hands-on/2026/08/15/hands-on-isolated-remote-development-with-ssh/) walks through another account on the same Mac, a LAN host, and a VPS from key generation through remote debugging.

This is particularly useful with AI-assisted editors. I can give the remote account the repository and tools it needs without quietly giving it every credential, configuration file, and personal artifact in my normal developer account. It is useful isolation, although it is not a security boundary by itself: shared groups, permissive files, `sudo`, system services, and mounted volumes still matter.

## What the Connection Looks Like

There are two related workflows, and I use both.

In a remote workspace, the editor connects over SSH, opens the repository in the target account, and runs its workspace extensions and debugger there. This is usually the simplest choice because the source paths and runtime paths already agree.

An attach session is different. The application is already running under the isolated account, `debugpy` is listening only on that host's loopback interface, and I forward the debugger port through SSH. I use this when I need to inspect a process launched by a service, test harness, scheduler, or command outside the editor.

| Workflow | Where the source is open | Where Python runs | When I use it |
| --- | --- | --- | --- |
| Remote workspace | In the remote SSH window | Under the remote or isolated account | Normal editing, testing, and debugging |
| SSH-tunneled attach | Locally or in a separate workspace | In an already-running remote process | Services, launchers, and hard-to-reproduce runtime behavior |

Both start with ordinary SSH access. If `ssh my-development-host` does not work reliably in a terminal, I do not ask the editor to conceal the problem.

## Create the Isolated Account

On macOS, I create a standard user in **System Settings → Users & Groups**. I then enable **Remote Login** under **General → Sharing** and allow access only for the accounts that actually need it. Apple documents the current control in its [Remote Login guide](https://support.apple.com/guide/mac-help/allow-a-remote-computer-to-access-your-mac-mchlp1066/mac).

For a same-machine connection, SSH can use `127.0.0.1`. The traffic never needs to leave the Mac, but authentication, account separation, and SSH port forwarding behave the same way they would on another host.

On Linux, the equivalent preparation is a dedicated non-root account and a running SSH server. I keep that account out of administrative groups unless the work genuinely requires elevated privileges.

## Set Up Key Authentication

I use an Ed25519 key and keep the private half on the machine where the editor runs. If I do not already have an appropriate key, I create one locally:

```bash
ssh-keygen -t ed25519 -C "remote-development"
```

I check the proposed filename before accepting it so I do not overwrite an existing key. A passphrase protects the private key at rest; `ssh-agent` or the macOS keychain can handle the repeated unlocks. The private key is never copied to the account being debugged.

The target account authorizes the public half. Where `ssh-copy-id` is available, the short path is:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub developer@host.example
```

If `ssh-copy-id` is unavailable, I display the public key locally:

```bash
cat ~/.ssh/id_ed25519.pub
```

I copy that single line and append it once to `~/.ssh/authorized_keys` while logged in as the target account. The usual permissions are deliberately restrictive:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

`authorized_keys` belongs to the account accepting the login. The public key may be installed for several isolated accounts or hosts, but each account retains its own file and can revoke access independently. OpenSSH will normally reject the file when the home directory, `.ssh` directory, or key file can be modified by other users; the [OpenSSH `sshd` manual](https://man.openbsd.org/sshd.8) explains that behavior.

## Give Each Destination a Stable Alias

The aliases in `~/.ssh/config` are the part that makes the arrangement pleasant to use. The editor, `ssh`, `scp`, `rsync`, Git, and port-forwarding commands can all refer to the same short name.

Here is a sanitized example. `192.0.2.0/24` is reserved for documentation; these are not addresses from my network.

```sshconfig
Host isolated-local
  HostName 127.0.0.1
  User isolateddev
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes

Host lab-mac
  HostName 192.0.2.20
  User isolateddev
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes

Host lab-linux
  HostName 192.0.2.30
  User isolateddev
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
```

`IdentityFile` selects the key for that destination. `IdentitiesOnly yes` tells OpenSSH not to offer every unrelated identity loaded in an agent, which avoids confusing authentication failures when several keys are available. The [OpenSSH client configuration manual](https://man.openbsd.org/ssh_config.5) is the authoritative reference for both settings.

Once the aliases exist, the same public key can be installed across several accounts without copying the private key or replacing each account's entire `authorized_keys` file:

```bash
for target in isolated-local lab-mac lab-linux; do
  ssh-copy-id -i ~/.ssh/id_ed25519.pub "$target"
done
```

I prefer this to synchronizing `authorized_keys` wholesale. A target may already trust another administrator, automation key, or recovery identity, and replacing the file would erase that access. Installing or removing individual public-key lines keeps each account's authorization independently reviewable.

Before opening an editor, I test the aliases directly:

```bash
ssh isolated-local
ssh lab-mac
ssh lab-linux
```

For a non-interactive check, I use `BatchMode` so an unexpected password prompt becomes a failure instead of silently changing the authentication method:

```bash
ssh -o BatchMode=yes isolated-local 'id; printf "SSH_OK\n"'
```

The reported user and home directory should belong to the isolated account. That small check has caught more mistakes for me than repeatedly clicking an editor's reconnect button.

This ordering is deliberate. Higher-level tools should consume ordinary SSH access rather than quietly configuring authentication on my behalf. I first make a small command such as `ssh user@host 'echo ok'` succeed, then involve the editor or debugger. Remote development is easier to diagnose when it follows the same rule: authenticate in a terminal first, connect the editor second, and debug the application third.

## Open the Host in VS Code, Cursor, or Windsurf

In VS Code, I install **Remote - SSH**, run **Remote-SSH: Connect to Host…** from the Command Palette, and select one of the aliases. The editor opens a new window, installs its server-side support under the remote account, and lets me open a folder from that account's filesystem. Microsoft's [Remote Development using SSH](https://code.visualstudio.com/docs/remote/ssh) documentation covers the current installation and connection flow.

Cursor, Windsurf, and other VS Code-derived editors follow the same basic model, but their compatible remote extension and command names can change. I use the remote SSH component supplied or recommended by that editor rather than assuming Microsoft's extension build is interchangeable. Once the editor reaches the point where it invokes the system SSH client, the aliases above remain the useful common layer.

Cursor has its own [Remote SSH support](https://cursor.com/changelog/0-35-x), and Windsurf documents its editor-specific SSH implementation and current limitations under [Advanced Configuration](https://docs.windsurf.com/windsurf/advanced). I check those product notes before installing an extension because compatibility changes faster than OpenSSH does. If an editor does not support a full remote workspace, the tunneled attach workflow later in this article still works: it depends on OpenSSH and `debugpy`, not on a particular editor's remote server.

The remote window is not merely a local editor looking at a network share. Workspace extensions, terminals, language servers, debug adapters, and many agent-side tools run under the remote account. That is exactly why the separate account is useful: its environment can be intentionally smaller than mine. It also means that a tool installed only in my normal account, or a local configuration file outside the repository, will not automatically exist in the remote session.

Once connected, I open the repository from the remote account's home directory and verify the environment in the integrated terminal:

```bash
whoami
printf '%s\n' "$HOME"
python3 --version
git status --short
```

## Debug Directly in the Remote Workspace

When the application can be launched from the editor, I prefer to debug it directly in the remote window. A small `.vscode/launch.json` is enough for a Python file:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Launch in Remote Workspace",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    }
  ]
}
```

Because both the editor workspace and Python process are remote, I do not need `pathMappings` for this case. Breakpoints refer to the same files the interpreter executes.

This is the path I recommend trying first. It gives me the remote account's interpreter, dependencies, environment variables, filesystem permissions, and services without opening a debugger port on the LAN.

## Attach to an Existing Python Process

Sometimes the process is started outside the editor. In that case I install `debugpy` in the target environment and start the application with the debugger bound to loopback:

```bash
python3 -m debugpy \
  --listen 127.0.0.1:5678 \
  --wait-for-client \
  ./app.py
```

`--wait-for-client` deliberately pauses startup until I attach. I omit it when blocking the process would be harmful and place a breakpoint later instead.

From my normal developer account, I forward a local port to the target account's loopback interface:

```bash
ssh -N -L 5678:127.0.0.1:5678 isolated-local
```

Changing `isolated-local` to `lab-mac` or `lab-linux` is the only difference for another machine. The editor still connects to `127.0.0.1:5678` locally; SSH carries that connection to the debugger without making port 5678 reachable from the rest of the network.

The attach configuration is:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Attach Through SSH",
      "type": "debugpy",
      "request": "attach",
      "connect": {
        "host": "127.0.0.1",
        "port": 5678
      },
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}",
          "remoteRoot": "/path/to/remote/project"
        }
      ]
    }
  ]
}
```

`pathMappings` matters only when the local and remote source paths differ. `localRoot` identifies the copy open in the editor; `remoteRoot` is the absolute project path reported by the Python process. Both copies must describe the same source revision or breakpoints and line numbers become misleading. Microsoft's [Python debugging documentation](https://code.visualstudio.com/docs/python/debugging) maintains the current `debugpy` attach syntax.

If I am already working in a Remote - SSH window, I can often avoid the separate terminal command by forwarding port 5678 from the editor's **Ports** view. The security model is the same: `debugpy` remains on remote loopback, and SSH owns the reachable path.

## A Small Helper for Conditional Attach

For applications where I occasionally need an in-process attachment point, I keep the helper boring and explicit:

```python
import debugpy


def wait_for_debugger(host: str = "127.0.0.1", port: int = 5678) -> None:
    debugpy.listen((host, port))
    print(f"Waiting for debugger on {host}:{port}")
    debugpy.wait_for_client()
    print("Debugger attached")
```

I call it only behind an explicit development flag. I do not let a production process unexpectedly stop at `wait_for_client()`, and I do not bind it to `0.0.0.0` merely because the target is remote. The SSH tunnel removes the need.

## Troubleshooting from the Bottom Up

When a remote editor fails, I start below the editor. This keeps an SSH authentication problem from masquerading as an IDE problem.

```bash
ssh -G isolated-local | rg '^(hostname|user|identityfile|identitiesonly) '
ssh -vv isolated-local
```

`ssh -G` shows the effective configuration after aliases and defaults have been applied. `ssh -vv` shows which keys are offered and why authentication succeeds or fails. On the target account, I check ownership and permissions:

```bash
ls -ld "$HOME" "$HOME/.ssh" "$HOME/.ssh/authorized_keys"
```

After terminal SSH works, I check the editor's Remote SSH output log. If the connection succeeds but Python tools do not appear, I verify that the Python and debugger extensions are installed in the remote workspace rather than only in the local editor.

For attach failures, I check each boundary separately: is `debugpy` listening on remote loopback, is the SSH forwarding session still running, is the local port already occupied, and do the source paths match? Changing all four at once makes the failure much harder to see.

## Security Boundaries I Keep

I never expose the debugger directly to an untrusted network. A Python debugger can inspect application memory and execute code in the target process; changing to an unusual port does not meaningfully protect it. I bind it to `127.0.0.1`, carry the connection through authenticated SSH, and stop it when the session is over.

I also keep the isolated account ordinary. It receives only the repository, dependencies, test data, and credentials required for the task. On macOS I do not grant remote users Full Disk Access merely to make setup easier. If the code needs access to a protected resource, I treat that as a separate decision rather than quietly weakening the account boundary.

Finally, I remember that SSH proves which key connected; it does not make the code safe. I still review what an editor extension or agent can execute, what the target account can read, and which network services it can reach.

## Where This Leaves the Workflow

The useful part of remote debugging is not port 5678. It is being able to reproduce the environment where the code actually runs while keeping the connection understandable enough to troubleshoot.

With a dedicated account, an `authorized_keys` entry, and a few clear aliases in `~/.ssh/config`, I can move between an isolated user on my Mac and a remote lab system without rewriting editor settings. VS Code, Cursor, Windsurf, and similar tools become clients of a connection I have already tested instead of opaque systems responsible for inventing one. From there, I can either debug directly in the remote workspace or attach through a tunnel when the process lifecycle demands it.

The step-by-step version is available in [Hands-On: Isolated Remote Development with SSH](/hands-on/2026/08/15/hands-on-isolated-remote-development-with-ssh/).
