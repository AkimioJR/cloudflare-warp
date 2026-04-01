import argparse
import shutil
from pathlib import Path
from asyncio import TaskGroup, to_thread, run


from utils import process_deb, ProcessResult
from get_latest_version import get_latest_version
from label import Distro, Arch


def parse_arch(value: str) -> Arch:
    try:
        return Arch(value)
    except ValueError as exc:
        valid = ", ".join(a.value for a in Arch.allCases())
        raise argparse.ArgumentTypeError(
            f"invalid arch: {value!r}. valid values: {valid}"
        ) from exc


def parse_distro(value: str) -> Distro:
    try:
        return Distro(value)
    except ValueError as exc:
        valid = ", ".join(d.value for d in Distro.allCases())
        raise argparse.ArgumentTypeError(
            f"invalid distro: {value!r}. valid values: {valid}"
        ) from exc


def process_result(result: ProcessResult, release_dir: Path):
    target_package = (
        release_dir / f"cloudflare-warp_{result.arch.value}_{result.distro.value}.deb"
    )
    print(f"Copied {result.package} -> {target_package}")
    shutil.copy2(result.package, target_package)

    for bin_name, info in result.bin_infos.items():
        target_bin_path = (
            release_dir / f"{bin_name}_{result.arch.value}_{result.distro.value}"
        )
        print(f"Copied {info.path} -> {target_bin_path}")
        shutil.copy2(info.path, target_bin_path)

        if result.distro == Distro.default:
            extra_bin_name = f"{bin_name}_{result.arch.value}"
            extra_bin_path = release_dir / extra_bin_name
            print(f"Copied {info.path} -> {extra_bin_path}")
            shutil.copy2(info.path, extra_bin_path)


async def process(
    distro: Distro,
    arch: Arch,
    dist_dir: Path,
    release_dir: Path,
    latest_version: str,
):
    result = await process_deb(distro, arch, dist_dir)
    if result.version != latest_version:
        print(
            f"⚠️ Skipping {distro} {arch} with version {result.version} (latest is {latest_version})"
        )
        return
    await to_thread(process_result, result, release_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sync Cloudflare WARP artifacts into dist when official version is newer"
    )
    parser.add_argument(
        "--arches",
        nargs="+",
        type=parse_arch,
        default=Arch.allCases(),
        help=f"Target CPU architectures (e.g. {', '.join(a.value for a in Arch.allCases())})",
    )
    parser.add_argument(
        "--distros",
        nargs="+",
        type=parse_distro,
        default=Distro.allCases(only_supported=True),
        help=f"Target distributions (e.g. {', '.join(d.value for d in Distro.allCases(only_supported=True))})",
    )
    parser.add_argument(
        "--dist-dir",
        default="dist",
        help="Output dist directory for deb and extracted binaries",
    )
    args = parser.parse_args()

    async def main():
        dist_dir = Path(args.dist_dir).resolve()
        release_dir = dist_dir / "release"

        release_dir.mkdir(parents=True, exist_ok=True)

        async with TaskGroup() as tg:
            latest_version, _ = await get_latest_version()
            for distro in args.distros:
                for arch in args.arches:
                    tg.create_task(
                        process(distro, arch, dist_dir, release_dir, latest_version)
                    )

    run(main())
