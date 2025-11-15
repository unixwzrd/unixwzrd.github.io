# Service Management

[← Back to Site Operations Guide](site-operations.md)

- [Service Management](#service-management)
  - [Jekyll Service Management](#jekyll-service-management)
    - [Using the Service Management Scripts](#using-the-service-management-scripts)
      - [1. **Site Service (Orchestrator)**](#1-site-service-orchestrator)
      - [2. **Jekyll Site (Standalone)**](#2-jekyll-site-standalone)
      - [3. **File Watcher (Standalone)**](#3-file-watcher-standalone)
    - [Service Management Options](#service-management-options)
      - [Refresh Control Flags](#refresh-control-flags)
      - [Verification Flags](#verification-flags)
      - [Service Selection Flags](#service-selection-flags)
      - [Default Behaviors](#default-behaviors)
    - [What the Service Scripts Do](#what-the-service-scripts-do)
    - [Service Status and Monitoring](#service-status-and-monitoring)

This section covers scripts and workflows for starting, stopping, and monitoring Jekyll and related services.

## Jekyll Service Management

### Using the Service Management Scripts

The project now uses a modular service management system with three main scripts:

#### 1. **Site Service (Orchestrator)**

The [utils/bin/site-service](../utils/bin/site-service) script manages both Jekyll and file watcher services:

```bash
# Start both services
./utils/bin/site-service start

# Start both services (fast mode, no OG refresh)
./utils/bin/site-service start -n

# Start both services (complete mode, with OG refresh)
./utils/bin/site-service start -r

# Restart both services (fast mode by default)
./utils/bin/site-service restart

# Restart both services (complete mode)
./utils/bin/site-service restart -r

# Stop both services
./utils/bin/site-service stop

# Manage individual services
./utils/bin/site-service -j start    # Jekyll only
./utils/bin/site-service -w start    # File watcher only
./utils/bin/site-service -j restart  # Restart Jekyll only

# Help
./utils/bin/site-service --help
```

#### 2. **Jekyll Site (Standalone)**

The [utils/bin/jekyll-site](../utils/bin/jekyll-site) script manages Jekyll independently:

```bash
# Start Jekyll server (complete mode)
./utils/bin/jekyll-site start

# Start Jekyll server (fast mode)
./utils/bin/jekyll-site start -n

# Restart Jekyll server (fast mode by default)
./utils/bin/jekyll-site restart

# Build once and run HTMLProofer link checks
./utils/bin/jekyll-site build -c
```

#### 3. **File Watcher (Standalone)**

The [utils/bin/file-watcher](../utils/bin/file-watcher) script manages the file watcher independently:

```bash
# Start file watcher
./utils/bin/file-watcher start

# Restart file watcher
./utils/bin/file-watcher restart

# Stop file watcher
./utils/bin/file-watcher stop
```

### Service Management Options

#### Refresh Control Flags

- `-n`: Fast mode (no OpenGraph refresh)
- `-r`: Complete mode (with OpenGraph refresh)

#### Verification Flags

- `-c`: Run HTMLProofer on the generated `_site/` output after each build (catches real 404s and missing anchors)

#### Service Selection Flags

- `-j`: Jekyll only
- `-w`: File watcher only

#### Default Behaviors

- By default, both services are started and managed together.

### What the Service Scripts Do

- **Site Service (Orchestrator)**: Manages both Jekyll and file watcher services.
- **Jekyll Site (Standalone)**: Manages Jekyll independently.
- **File Watcher (Standalone)**: Manages the file watcher independently.

### Service Status and Monitoring

- Use the service scripts to check status, restart, or stop services as needed.
