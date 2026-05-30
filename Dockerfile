FROM debian:trixie-slim

# /run/cloudflare-warp 是 cloudflare-warp 的默认运行时目录
# /var/lib/cloudflare-warp 是默认数据目录
# /var/log/cloudflare-warp 是默认日志目录
VOLUME ["/run/cloudflare-warp", "/var/lib/cloudflare-warp", "/var/log/cloudflare-warp"] 

ENV WARP_PROXY_LISTEN_PORT=4000 \
    WARP_PROXY_LISTEN_IP=0.0.0.0 \
    WARP_PROXY_TARGET_PORT=50000

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gpg \
        socat \
    && curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg \
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

ENTRYPOINT ["/entrypoint.sh"]
