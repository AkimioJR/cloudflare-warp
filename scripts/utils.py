import shutil
from dataclasses import dataclass
from pathlib import Path
from hashlib import sha256
from tempfile import TemporaryDirectory

from httpx import AsyncClient
from aiofiles import open as async_open

from get_latest_version import get_latest_version
from extract_bin import extract_warp_binaries_from_deb
from label import Distro, Arch


async def calculate_sha256(file_path: Path, block_size: int = 2**16) -> str:
    """
    calculate_sha256 computes the SHA256 hash of the file at the given path.
    """
    sha256_hash = sha256()

    async with async_open(file_path, "rb") as f:
        while True:
            byte_block = await f.read(block_size)
            if not byte_block:
                break
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


async def download_file(client: AsyncClient, url: str, destination: Path) -> None:
    headers: dict[str, str] = {
        "User-Agent": "Debian APT-HTTP/1.3 (2.6.1)",
        "Accept": "application/octet-stream,*/*;q=0.9",
        "Connection": "close",
    }
    async with (
        async_open(destination, "wb") as f,
        client.stream("GET", url, headers=headers, timeout=60) as res,
    ):
        res.raise_for_status()
        async for chunk in res.aiter_bytes():
            await f.write(chunk)


def safe_version_label(version: str) -> str:
    return version.replace("/", "_")


@dataclass
class ProcessResult:
    @dataclass
    class BinaryInfo:
        path: Path
        sha256: str

    version: str
    distro: Distro
    arch: Arch
    dir: Path
    package: Path
    bin_infos: dict[str, BinaryInfo]


async def process_deb(distro: Distro, arch: Arch, dist_dir: Path) -> ProcessResult:
    version, url = await get_latest_version(distro, arch)
    dist_dir = dist_dir / distro.value / arch.value
    dist_dir.mkdir(parents=True, exist_ok=True)
    deb_name = (
        f"cloudflare-warp_{safe_version_label(version)}_{distro.value}_{arch.value}.deb"
    )
    target_deb = dist_dir / deb_name
    print(f"Downloading {distro.value} {arch.value} -> {deb_name}")

    async with AsyncClient() as client:
        await download_file(client, url, target_deb)
        bin_dir = dist_dir / "bin"
        bin_dir.mkdir(parents=True, exist_ok=True)
        print(f"Extracting binaries from {deb_name} -> {bin_dir}")
        bin_infos: dict[str, ProcessResult.BinaryInfo] = {}
        with TemporaryDirectory() as tmpdir:
            result = await extract_warp_binaries_from_deb(target_deb, Path(tmpdir))
            for name, src in result.items():
                target_path = (
                    bin_dir
                    / f"{name}_{safe_version_label(version)}_{distro.value}_{arch.value}"
                )
                shutil.copy2(src, target_path)
                bin_infos[name] = ProcessResult.BinaryInfo(
                    path=target_path,
                    sha256=await calculate_sha256(target_path),
                )

    return ProcessResult(
        version=version,
        distro=distro,
        arch=arch,
        dir=dist_dir,
        package=target_deb,
        bin_infos=bin_infos,
    )
