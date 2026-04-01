import json
import urllib.error
import urllib.request
from compare_versions import compare_versions

from get_latest_version import get_latest_version


def get_repo_latest_release_tag(owner: str, repo: str) -> str | None:
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "cloudflare-warp-sync-script",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            tag = payload.get("tag_name")
            if isinstance(tag, str) and tag.strip():
                return tag.strip()
            return None
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def normalize_version(version: str | None) -> str | None:
    if not version:
        return None
    return version.removeprefix("v").strip()


if __name__ == "__main__":
    official_version = str(normalize_version(get_latest_version()[0]))
    repo_version = normalize_version(
        get_repo_latest_release_tag("AkimioJR", "cloudflare-warp")
    )

    needs_sync = (
        repo_version is None or compare_versions(official_version, repo_version) != 0
    )

    result = {
        "official_version": official_version,
        "repo_version": repo_version,
        "needs_sync": needs_sync,
    }
    print(json.dumps(result, indent=2))
