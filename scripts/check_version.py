import json
import os

from compare_versions import compare_versions
from get_latest_version import get_latest_version
from httpx import AsyncClient, HTTPStatusError

REPO_OWNER = "AkimioJR"
REPO_NAME = "cloudflare-warp"


async def get_repo_latest_release_tag(owner: str, repo: str) -> str | None:
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "cloudflare-warp-sync-script",
    }
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"

    try:
        async with AsyncClient() as client:
            resp = await client.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        tag = resp.json().get("tag_name")
    except HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return None
        if exc.response.status_code == 403:
            raise RuntimeError(
                f"GitHub API rate limit exceeded while fetching {url}; "
                "set GITHUB_TOKEN to raise the limit"
            ) from exc
        raise
    if isinstance(tag, str) and tag.strip():
        return tag.strip()
    return None


def normalize_version(version: str | None) -> str | None:
    if not version:
        return None
    return version.removeprefix("v").strip()


if __name__ == "__main__":
    from asyncio import run

    async def main():
        official_version, _ = await get_latest_version()
        official_version = str(normalize_version(official_version))
        repo_version = normalize_version(
            await get_repo_latest_release_tag(REPO_OWNER, REPO_NAME)
        )

        needs_sync = (
            repo_version is None
            or compare_versions(official_version, repo_version) != 0
        )

        result = {
            "official_version": official_version,
            "repo_version": repo_version,
            "needs_sync": needs_sync,
        }
        print(json.dumps(result, indent=2))

    run(main())
