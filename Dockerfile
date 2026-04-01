FROM debian:trixie

# /run/cloudflare-warp 是 cloudflare-warp 的默认运行时目录
# /var/lib/cloudflare-warp 是默认数据目录
# /var/log/cloudflare-warp 是默认日志目录
VOLUME ["/var/lib/cloudflare-warp", "/var/log/cloudflare-warp"] 

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN apt-get update && apt-get install -y lsb-release curl gpg ca-certificates socat

RUN curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg \
    | gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg

RUN tee /etc/apt/sources.list.d/cloudflare-warp.sources << EOF
Types: deb
URIs: https://pkg.cloudflareclient.com/
Suites: trixie
Components: main
Signed-By: /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg
EOF

RUN apt-get update && apt-get install -y cloudflare-warp

ENTRYPOINT ["/entrypoint.sh"]