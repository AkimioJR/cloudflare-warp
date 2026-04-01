import argparse
from pathlib import Path
import shutil

from utils import process_deb, ProcessResult
from get_latest_version import get_latest_version


SUPPORT_DISTRO_MAP = {
    "trixie": "Trixie (13)",
    "bookworm": "Bookworm (12)",
    "bullseye": "Bullseye (11)",
    # "buster": "Buster (10)",
    # "stretch": "Stretch (9)",
    "noble": "Noble (24.04)",
    "jammy": "Jammy (22.04)",
    "focal": "Focal (20.04)",
    # "bionic": "Bionic (18.04)",
    # "xenial": "Xenial (16.04)",
}


def generate_distro_map(distros: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for d in distros:
        label = SUPPORT_DISTRO_MAP.get(d)
        if label:
            result[d] = label
    return result


DEFAULT_ARCHES = [
    "amd64",
    "arm64",
]


def unique_release_path(release_dir: Path, file_name: str) -> Path:
    """Return a non-conflicting target path under release_dir."""
    candidate = release_dir / file_name
    if not candidate.exists():
        return candidate

    stem = candidate.stem
    suffix = candidate.suffix
    index = 1
    while True:
        candidate = release_dir / f"{stem}__dup{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def copy_to_release(src: Path, release_dir: Path, target_name: str) -> Path:
    dst = unique_release_path(release_dir, target_name)
    shutil.copy2(src, dst)
    return dst


def main():
    parser = argparse.ArgumentParser(
        description="Sync Cloudflare WARP artifacts into dist when official version is newer"
    )
    parser.add_argument(
        "--arches",
        nargs="+",
        default=DEFAULT_ARCHES,
        help="Target CPU architectures (e.g., amd64 arm64 armhf)",
    )
    parser.add_argument(
        "--distro",
        nargs="+",
        default=list(SUPPORT_DISTRO_MAP.keys()),
        help="Target distributions (e.g., trixie bookworm bullseye)",
    )
    parser.add_argument(
        "--dist-dir",
        default="dist",
        help="Output dist directory for deb and extracted binaries",
    )
    args = parser.parse_args()

    dist_dir = Path(args.dist_dir).resolve()
    release_dir = dist_dir / "release"

    release_dir.mkdir(parents=True, exist_ok=True)

    latest_version = get_latest_version()[0]

    errors: list[str] = []
    results: list[ProcessResult] = []

    for distro in generate_distro_map(args.distro).keys():
        for arch in args.arches:
            try:
                result = process_deb(distro, arch, dist_dir)
                if result.version == latest_version:
                    results.append(result)
                else:
                    print(
                        f"⚠️ Skipping {distro} {arch} with version {result.version} (latest is {latest_version})"
                    )
            except Exception as e:
                errors.append(f"{distro} {arch}: {e}")

    if not results:
        print("No artifacts were processed.")
        if errors:
            print("Errors:")
            for err in errors:
                print(f"  - {err}")
        return 1

    for item in results:
        package_name = item.package.name
        copy_to_release(item.package, release_dir, package_name)

    by_arch: dict[str, list[ProcessResult]] = {}
    for item in results:
        by_arch.setdefault(item.arch, []).append(item)

    for arch, arch_results in by_arch.items():
        trixie_result = next((r for r in arch_results if r.distro == "trixie"), None)
        if trixie_result is None:
            errors.append(f"{arch}: no trixie baseline found for binary sha compare")
            continue

        baseline_sha: dict[str, str] = {}
        for bin_name, info in trixie_result.bin_infos.items():
            baseline_sha[bin_name] = info.sha256
            baseline_target_name = f"{bin_name}_{arch}_trixie_{trixie_result.version}"
            copy_to_release(info.path, release_dir, baseline_target_name)

        # Copy extra binaries only when sha differs from trixie baseline.
        for item in arch_results:
            if item.distro == "trixie":
                continue

            for bin_name, info in item.bin_infos.items():
                ref_sha = baseline_sha.get(bin_name)
                if ref_sha is None:
                    errors.append(
                        f"{item.distro}/{arch}: missing baseline sha for {bin_name}"
                    )
                    continue

                if info.sha256 != ref_sha:
                    extra_target_name = f"{bin_name}_{arch}_{item.distro}_{item.version}_{info.sha256[:8]}"
                    copy_to_release(info.path, release_dir, extra_target_name)

    if errors:
        print("❌ Finished with errors:")
        for err in errors:
            print(f"  - {err}")
        return 1
    else:
        print("✅ Finished without errors.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
