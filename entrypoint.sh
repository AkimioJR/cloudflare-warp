#!/bin/bash
set -euo pipefail

# ── 环境变量默认值 ────────────────────────────────────────────────────
WARP_PROXY_LISTEN_PORT="${WARP_PROXY_LISTEN_PORT:-4000}"
WARP_PROXY_LISTEN_IP="${WARP_PROXY_LISTEN_IP:-0.0.0.0}"
WARP_PROXY_TARGET_PORT="${WARP_PROXY_TARGET_PORT:-50000}"

# ── 为 systemd 服务写入环境变量文件 ───────────────────────────────────
cat > /etc/default/cloudflare-warp <<EOF
WARP_PROXY_LISTEN_PORT=${WARP_PROXY_LISTEN_PORT}
WARP_PROXY_LISTEN_IP=${WARP_PROXY_LISTEN_IP}
WARP_PROXY_TARGET_PORT=${WARP_PROXY_TARGET_PORT}
EOF

# ── 根据 WARP_MEMORY_MAX 生成内存限制 drop-in ────────────────────────
if [[ -n "${WARP_MEMORY_MAX:-}" ]]; then
    mkdir -p /etc/systemd/system/warp-svc.service.d
    cat > /etc/systemd/system/warp-svc.service.d/memory-limit.conf <<EOF
[Service]
MemoryMax=${WARP_MEMORY_MAX}
EOF
    echo "[entrypoint] Memory limit set: MemoryMax=${WARP_MEMORY_MAX}"
fi

# ── 启用 systemd 服务 ─────────────────────────────────────────────────
systemctl enable warp-svc.service
systemctl enable socat.service
systemctl enable warp-restart.timer

echo "[entrypoint] Starting systemd..."
exec /lib/systemd/systemd --system
