FROM debian:trixie-slim

# /run/cloudflare-warp 是 cloudflare-warp 的默认运行时目录
# /var/lib/cloudflare-warp 是默认数据目录
# /var/log/cloudflare-warp 是默认日志目录
VOLUME ["/run/cloudflare-warp", "/var/lib/cloudflare-warp", "/var/log/cloudflare-warp"]

ENV WARP_PROXY_LISTEN_PORT=4000 \
    WARP_PROXY_LISTEN_IP=0.0.0.0 \
    WARP_PROXY_TARGET_PORT=50000

# Install systemd and base dependencies
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        dbus \
        gpg \
        iproute2 \
        socat \
        systemd \
        systemd-sysv \
    && rm -rf /var/lib/apt/lists/*

# Install Cloudflare WARP
RUN curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg \
        | gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg \
    && printf '%s\n' \
        'Types: deb' \
        'URIs: https://pkg.cloudflareclient.com/' \
        'Suites: trixie' \
        'Components: main' \
        'Signed-By: /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg' \
        > /etc/apt/sources.list.d/cloudflare-warp.sources \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends cloudflare-warp \
    && rm -rf /var/lib/apt/lists/*

# Disable unnecessary systemd services for container environment
RUN systemctl mask \
        getty@.service \
        serial-getty@.service \
        systemd-logind.service \
        systemd-remount-fs.service \
        systemd-modules-load.service \
        systemd-resolved.service \
        systemd-networkd.service \
    && systemctl set-default multi-user.target

# Install systemd unit files
COPY config/systemd/ /lib/systemd/system/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/sbin/init"]
