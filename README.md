# cloudflare-warp

Automatically tracks Cloudflare WARP Linux package releases, publishes extracted
release artifacts, and builds a multi-arch Docker image.

## What This Repository Does

- Checks the official Cloudflare WARP APT repository on a schedule.
- Publishes a GitHub Release when a new WARP version is available.
- Uploads `.deb` packages and extracted `warp-cli` / `warp-svc` binaries.
- Extracts and commits the upstream Cloudflare WARP changelog.
- Builds and pushes Docker images for `linux/amd64` and `linux/arm64/v8`.

## Docker Image

The image is published to Docker Hub:

```sh
docker pull akimio/cloudflare-warp:latest
```

Versioned releases are also tagged with the Cloudflare WARP package version:

```sh
docker pull akimio/cloudflare-warp:<version>
```

The image is based on `debian:trixie-slim` and installs Cloudflare WARP from
Cloudflare's official APT repository.

### Process Management

The container uses **systemd** as PID 1 to manage `warp-svc` and the `socat`
proxy. systemd provides:

- Automatic restart on crash (`Restart=always`).
- Cgroup-based memory limits via `MemoryMax` / `MemoryHigh`.
- A periodic restart timer (`warp-restart.timer`) that restarts `warp-svc` every
  6 hours to mitigate the known [WARP memory leak][warp-leak].

[warp-leak]: https://noorkhafidzin.com/posts/solving-cloudflare-warp-memory-leaks-with-systemd-auto-restart/

## Docker Compose

An example Compose file is included:

```sh
docker compose up -d
```

The container needs `SYS_ADMIN` and `NET_ADMIN` capabilities, access to
`/dev/net/tun`, and a tmpfs mount on `/run` for systemd. The included
`compose.yaml` configures all of these.

## Environment Variables

| Variable | Default | Description |
| --- | --- | --- |
| `WARP_PROXY_LISTEN_IP` | `0.0.0.0` | IP address that `socat` listens on. |
| `WARP_PROXY_LISTEN_PORT` | `4000` | Port exposed for clients to connect to. |
| `WARP_PROXY_TARGET_PORT` | `50000` | Local Cloudflare WARP proxy port to forward to. |
| `WARP_MEMORY_MAX` | _(none)_ | Memory limit for `warp-svc`. Accepts `K`, `M`, `G` suffixes (e.g. `512M`). When set, the entrypoint creates a systemd drop-in that applies `MemoryMax`. When unset, the default service unit uses `MemoryMax=512M`. |

Example:

```yaml
environment:
  WARP_PROXY_LISTEN_IP: 0.0.0.0
  WARP_PROXY_LISTEN_PORT: 4000
  WARP_PROXY_TARGET_PORT: 50000
  WARP_MEMORY_MAX: 512M
```

## Automation

The workflows are split by responsibility:

- `check.yaml` checks whether Cloudflare WARP has a new version.
- `release.yaml` downloads artifacts, commits `CHANGELOG.md`, and publishes a GitHub Release.
- `docker.yaml` builds and pushes the multi-arch Docker image.

When a scheduled check finds a new version, the release workflow runs and then
publishes Docker tags for both `latest` and the detected version. Manually
running the Docker workflow by itself publishes `latest` unless a version tag is
explicitly requested.

## Local Scripts

Use `uv` for local Python execution:

```sh
uv sync --frozen
uv run scripts/check_version.py
uv run scripts/release.py
```

Generated release assets are written under `dist/release`.
