import gzip
from io import BytesIO
from asyncio import sleep

from httpx import AsyncClient

from compare_versions import compare_versions
from label import Distro, Arch


async def get_latest_version(
    distro: Distro = Distro.default,
    arch: Arch = Arch.default,
    max_retries: int = 3,
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
    for attempt in range(max_retries):
        try:
            async with AsyncClient() as client:
                response = await client.get(repo_url, headers=headers, timeout=10)
            response.raise_for_status()
            with gzip.GzipFile(fileobj=BytesIO(response.content)) as f:
                content = f.read().decode("utf-8")
            break
        except Exception as e:
            last_error = e
            await sleep((1 + attempt) * 3)

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
    import argparse
    from asyncio import run

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

    async def main():
        version, url = await get_latest_version(args.distro, args.arch)
        print(f"Latest version: {version}")
        print(f"Download URL: {url}")

    run(main())
