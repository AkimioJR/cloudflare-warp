import shutil
import tarfile
from io import BytesIO
from pathlib import Path
from typing import AsyncIterator
from asyncio import to_thread

from aiofiles import open as async_open


async def __iter_ar_members(archive_path: Path) -> AsyncIterator[tuple[str, bytes]]:
    """
    Asynchronously yield (member_name, member_data) from a Unix ar archive.
    """
    async with async_open(archive_path, "rb") as f:
        magic = await f.read(8)
        if magic != b"!<arch>\n":
            raise RuntimeError(f"invalid deb/ar file: {archive_path}")

        while True:
            header = await f.read(60)
            if not header:
                break
            if len(header) < 60:
                raise RuntimeError(f"truncated ar header in: {archive_path}")

            raw_name = header[0:16].decode("utf-8", errors="replace")
            raw_size = header[48:58].decode("ascii", errors="replace").strip()
            trailer = header[58:60]

            if trailer != b"`\n":
                raise RuntimeError(f"corrupt ar member header in: {archive_path}")

            try:
                member_size = int(raw_size)
            except ValueError as exc:
                raise RuntimeError(
                    f"invalid member size in ar archive: {raw_size}"
                ) from exc

            member_data = await f.read(member_size)
            if len(member_data) != member_size:
                raise RuntimeError(f"truncated ar member payload in: {archive_path}")

            # Members are 2-byte aligned.
            if member_size % 2 == 1:
                await f.read(1)

            name = raw_name.strip()
            if name.startswith("#1/"):
                # BSD variant: filename is prefixed in file data.
                name_len = int(name[3:])
                name_bytes = member_data[:name_len]
                name = name_bytes.decode("utf-8", errors="replace")
                member_data = member_data[name_len:]
            else:
                # Common GNU/System V variant, often ends with '/'.
                if name.endswith("/"):
                    name = name[:-1]

            yield name, member_data


async def extract_warp_binaries_from_deb(
    deb_path: Path, output_dir: Path
) -> dict[str, Path]:
    """Extract `warp-cli` and `warp-svc` binaries from a .deb package.

    Args:
            deb_path: Path to the .deb file.
            output_dir: Directory to place extracted binaries.

    Returns:
            Mapping of binary name -> extracted absolute Path.

    Raises:
            FileNotFoundError: If deb file or target binaries are missing.
            RuntimeError: If the deb format is invalid or extraction fails.
    """
    deb_path = Path(deb_path).expanduser().resolve()
    out_dir = Path(output_dir).expanduser().resolve()

    if not deb_path.is_file():
        raise FileNotFoundError(f"deb file not found: {deb_path}")

    out_dir.mkdir(parents=True, exist_ok=True)

    data_tar_member = None
    async for member_name, member_data in __iter_ar_members(deb_path):
        if member_name.startswith("data.tar"):
            data_tar_member = member_data
            break

    if data_tar_member is None:
        raise FileNotFoundError(f"data.tar.* not found in deb: {deb_path}")

    candidates = {
        "warp-cli": [
            "bin/warp-cli",
            "usr/bin/warp-cli",
            "./bin/warp-cli",
            "./usr/bin/warp-cli",
        ],
        "warp-svc": [
            "bin/warp-svc",
            "usr/bin/warp-svc",
            "./bin/warp-svc",
            "./usr/bin/warp-svc",
        ],
    }

    def _sync_extract() -> dict[str, Path]:
        extracted: dict[str, Path] = {}
        with tarfile.open(fileobj=BytesIO(data_tar_member), mode="r:*") as tf:
            for binary_name, paths in candidates.items():
                member = next(
                    (tf.getmember(p) for p in paths if p in tf.getnames()), None
                )
                if member is None:
                    searched = ", ".join(paths)
                    raise FileNotFoundError(
                        f"{binary_name} not found in deb payload. searched: {searched}"
                    )

                src = tf.extractfile(member)
                if src is None:
                    raise RuntimeError(f"failed to read member data: {member.name}")

                dst = out_dir / binary_name
                with dst.open("wb") as f:
                    shutil.copyfileobj(src, f)

                if member.mode:
                    dst.chmod(member.mode)
                extracted[binary_name] = dst
        return extracted

    return await to_thread(_sync_extract)


if __name__ == "__main__":
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="Extract warp-cli and warp-svc binaries from a .deb package"
    )
    parser.add_argument(
        "--deb-path",
        "--deb_path",
        dest="deb_path",
        type=str,
        required=True,
        help="Path to the .deb file to extract from",
    )
    parser.add_argument(
        "--output-dir",
        "--output_dir",
        dest="output_dir",
        type=str,
        required=False,
        default="extracted_bins",
        help="Directory to place extracted binaries",
    )

    args = parser.parse_args()

    async def main():
        try:
            result = await extract_warp_binaries_from_deb(
                args.deb_path, args.output_dir
            )
            for name, path in result.items():
                print(f"Extracted {name} to: {path}")
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())
