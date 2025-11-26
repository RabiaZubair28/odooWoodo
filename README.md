# Sindh HRMIS

**Version:** 0.1.0
**Description:** HR Management Information System for Sindh Government
**Python Version:** 3.12+

## Overview

This project is an Odoo 18.0 implementation designed for HR management. It utilizes a containerized architecture with Docker and Docker Compose, employing `uv` for high-performance Python dependency management.

## Prerequisites

  * Docker Engine
  * Docker Compose

## Architecture

The project uses a multi-stage `Dockerfile` to separate build dependencies from runtime requirements.

| Stage | Description |
| :--- | :--- |
| **Builder** | Compiles system dependencies (libldap, libsasl), installs `uv`, and builds the Odoo environment. |
| **Dev** | Inherits from Builder. Adds development tools (wkhtmltopdf) and mounts local source code for live reloading. |
| **Prod** | Inherits from `debian:bookworm-slim`. Copies only compiled artifacts from Builder. Optimized for security and size. |

## Usage

A wrapper script `run.sh` is provided to manage the environment context and Docker Compose overrides.

### Development Mode

To start the system in development mode (hot-reloading enabled, local modules mounted):

```bash
./run.sh
```

  * **Web Interface:** http://localhost:8069
  * **Debugger:** Port 5678 is exposed for remote debugging.
  * **Logs:** `docker compose logs -f odoo`

### Production Mode

To start the system in production mode (immutable image, optimized runtime, no code mounting):

```bash
./run.sh --prod
```

  * **Note:** This mode uses `.env.prod` and `compose.prod.yml`.

## Configuration

Configuration is managed via the `.env` file (bundled for development). The `compose.yml` file relies on the following key environment variables:

  * **Database:** `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
  * **Odoo Runtime:** `ODOO_WORKERS`, `ODOO_LIMIT_MEMORY_HARD`, `ODOO_LIMIT_MEMORY_SOFT`, `LOG_LEVEL`

## Development Tools

The project uses `pyproject.toml` to configure static analysis tools.

  * **Linter:** `ruff` (Target Python 3.12, Line length 88)
  * **Type Checker:** `pyright` (Strictness configured for `modules` directory)

To run these tools locally (requires `uv` installed):

```bash
uv run ruff check .
uv run pyright
```

## Dependencies

Key libraries managed via `pyproject.toml` and `uv`:

  * `numpy`, `pandas` (Data processing)
  * `openpyxl`, `xlsxwriter`, `xlrd` (Excel I/O)
  * `odoo-stubs` (Type support)

To update dependencies, modify `pyproject.toml` and restart the container via `./run.sh` to trigger a rebuild.
