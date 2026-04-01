import urllib.request
import urllib.error
import gzip
from io import BytesIO
import argparse
import time

from compare_versions import compare_versions

from label import Distro, Arch


def get_latest_version(
    distro: Distro = Distro.default, arch: Arch = Arch.default
) -> tuple[str, str]:
    """
    get the latest version of the cloudflare-warp package and its download link
    """
    repo_url = f"https://pkg.cloudflareclient.com/dists/{distro.value}/main/binary-{arch.value}/Packages.gz"

    headers = {
        "User-Agent": "Debian APT-HTTP/1.3 (2.6.1)",
        "Accept": "application/gzip,*/*;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    }

    content = None
    last_error = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(repo_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                raw = response.read()
            with gzip.GzipFile(fileobj=BytesIO(raw)) as f:
                content = f.read().decode("utf-8")
            break
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
            last_error = e
            if attempt < 2:
                time.sleep(1 + attempt)

    if content is None:
        raise last_error if last_error else RuntimeError("download Packages.gz failed")

    packages = content.strip().split("\n\n")

    latest_version: str | None = None
    latest_filename: str | None = None

    for pkg_block in packages:
        pkg_info: dict[str, str] = {}
        for line in pkg_block.split("\n"):
            if ": " in line:
                key, value = line.split(": ", 1)
                pkg_info[key.strip()] = value.strip()

        if (
            pkg_info.get("Package") == "cloudflare-warp"
            and pkg_info.get("Architecture") == arch.value
        ):
            version = pkg_info.get("Version")
            filename = pkg_info.get("Filename")
            if version and filename:
                if (
                    latest_version is None
                    or compare_versions(version, latest_version) > 0
                ):
                    latest_version = version
                    latest_filename = filename

    if latest_version and latest_filename:
        download_url = f"https://pkg.cloudflareclient.com/{latest_filename}"
        return (latest_version, download_url)

    raise RuntimeError(
        f"failed to find cloudflare-warp package in {distro}/{arch} repository"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get Cloudflare WARP latest version info"
    )
    parser.add_argument(
        "--distro",
        type=str,
        default="trixie",
        help="distribution codename (e.g., trixie, bookworm, noble, jammy)",
    )
    parser.add_argument(
        "--arch",
        type=str,
        default="amd64",
        help="CPU architecture (e.g., amd64, arm64, armhf)",
    )

    args = parser.parse_args()

    print(get_latest_version(args.distro, args.arch))
