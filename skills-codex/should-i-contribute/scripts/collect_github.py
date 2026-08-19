#!/usr/bin/env python3
"""Collect reproducible, read-only GitHub contribution-health evidence."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


API = "https://api.github.com"
OUTSIDE = {"NONE", "FIRST_TIMER", "FIRST_TIME_CONTRIBUTOR", "CONTRIBUTOR"}
NEWCOMER = {"FIRST_TIMER", "FIRST_TIME_CONTRIBUTOR"}
CORE = {"OWNER", "MEMBER", "COLLABORATOR"}


class CollectionError(RuntimeError):
    pass


def normalize_repo(value: str) -> str:
    raw = value.strip().rstrip("/")
    if "://" in raw:
        parsed = urllib.parse.urlparse(raw)
        if parsed.hostname not in {"github.com", "www.github.com"}:
            raise CollectionError("collect_github.py supports github.com URLs only")
        raw = parsed.path.strip("/")
    elif raw.startswith("git@github.com:"):
        raw = raw.split(":", 1)[1]
    if raw.endswith(".git"):
        raw = raw[:-4]
    parts = raw.split("/")
    if len(parts) != 2 or not all(parts):
        raise CollectionError("repository must be OWNER/REPO or a github.com repository URL")
    return f"{parts[0]}/{parts[1]}"


def discover_token() -> str | None:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token.strip()
    if not shutil.which("gh"):
        return None
    result = subprocess.run(
        ["gh", "auth", "token"], capture_output=True, text=True, timeout=10, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else None


class GitHub:
    def __init__(self, token: str | None) -> None:
        self.token = token
        self.requests = 0

    def get(
        self, path: str, params: dict[str, Any] | None = None, allowed: set[int] | None = None
    ) -> tuple[int, Any, dict[str, str]]:
        query = urllib.parse.urlencode(params or {})
        url = f"{API}/{path.lstrip('/')}" + (f"?{query}" if query else "")
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "should-i-contribute-skill",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(url, headers=headers)
        for attempt in range(3):
            self.requests += 1
            try:
                with urllib.request.urlopen(request, timeout=20) as response:
                    body = response.read().decode("utf-8")
                    data = json.loads(body) if body else None
                    return response.status, data, dict(response.headers.items())
            except urllib.error.HTTPError as error:
                body = error.read().decode("utf-8", errors="replace")
                if allowed and error.code in allowed:
                    return error.code, None, dict(error.headers.items())
                if error.code in {429, 502, 503, 504} and attempt < 2:
                    time.sleep(2**attempt)
                    continue
                remaining = error.headers.get("X-RateLimit-Remaining")
                suffix = " GitHub API rate limit is exhausted." if remaining == "0" else ""
                raise CollectionError(
                    f"GitHub API {error.code} for {url}: {body[:300]}{suffix}"
                ) from error
            except urllib.error.URLError as error:
                if attempt < 2:
                    time.sleep(2**attempt)
                    continue
                raise CollectionError(f"GitHub request failed for {url}: {error.reason}") from error
        raise CollectionError(f"GitHub request failed for {url}")

    def paginate(
        self, path: str, params: dict[str, Any] | None = None, max_pages: int = 20
    ) -> tuple[list[dict[str, Any]], bool]:
        items: list[dict[str, Any]] = []
        base = dict(params or {})
        for page in range(1, max_pages + 1):
            status, data, _ = self.get(path, {**base, "per_page": 100, "page": page})
            if status != 200 or not isinstance(data, list):
                raise CollectionError(f"unexpected paginated response from {path}")
            items.extend(data)
            if len(data) < 100:
                return items, False
        return items, True

    def search(self, query: str, page: int = 1) -> dict[str, Any]:
        status, data, _ = self.get(
            "search/issues", {"q": query, "per_page": 100, "page": page}
        )
        if status != 200 or not isinstance(data, dict):
            raise CollectionError("unexpected search response")
        return data


def iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def closed_query(repo: str, start: datetime, end: datetime) -> str:
    return f"repo:{repo} is:pr is:closed closed:{iso(start)}..{iso(end)}"


def collect_closed(
    github: GitHub, repo: str, start: datetime, end: datetime
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    top = github.search(closed_query(repo, start, end))
    expected = int(top["total_count"])
    incomplete = bool(top.get("incomplete_results"))

    def collect_slice(left: datetime, right: datetime) -> list[dict[str, Any]]:
        probe = github.search(closed_query(repo, left, right))
        total = int(probe["total_count"])
        nonlocal incomplete
        incomplete = incomplete or bool(probe.get("incomplete_results"))
        if total > 1000:
            seconds = int((right - left).total_seconds())
            if seconds < 2:
                raise CollectionError("more than 1,000 PRs closed within one second")
            midpoint = left + timedelta(seconds=seconds // 2)
            return collect_slice(left, midpoint) + collect_slice(
                midpoint + timedelta(seconds=1), right
            )
        result = list(probe.get("items", []))
        for page in range(2, (total + 99) // 100 + 1):
            result.extend(github.search(closed_query(repo, left, right), page).get("items", []))
        return result

    raw = collect_slice(start, end) if expected else []
    by_number = {int(item["number"]): item for item in raw}
    return list(by_number.values()), {
        "expected": expected,
        "fetched": len(by_number),
        "complete": len(by_number) == expected and not incomplete,
        "incomplete_results": incomplete,
    }


def is_bot(item: dict[str, Any]) -> bool:
    return (item.get("user") or {}).get("type") == "Bot"


def association(item: dict[str, Any]) -> str:
    return str(item.get("author_association") or "UNKNOWN")


def population(items: list[dict[str, Any]]) -> dict[str, Any]:
    humans = [item for item in items if not is_bot(item)]
    counts = Counter(association(item) for item in humans)
    return {
        "all": len(items),
        "bots_excluded": len(items) - len(humans),
        "humans": len(humans),
        "outside": sum(counts[name] for name in OUTSIDE),
        "newcomers": sum(counts[name] for name in NEWCOMER),
        "core": sum(counts[name] for name in CORE),
        "unknown": sum(n for name, n in counts.items() if name not in OUTSIDE | CORE),
        "by_author_association": dict(sorted(counts.items())),
    }


def ratio(numerator: int, denominator: int) -> dict[str, Any]:
    return {
        "numerator": numerator,
        "denominator": denominator,
        "percent": round(numerator / denominator * 100, 1) if denominator else None,
    }


def closed_outcomes(items: list[dict[str, Any]]) -> dict[str, Any]:
    humans = [item for item in items if not is_bot(item)]

    def merged(item: dict[str, Any]) -> bool:
        return bool((item.get("pull_request") or {}).get("merged_at"))

    def group(names: set[str]) -> list[dict[str, Any]]:
        return [item for item in humans if association(item) in names]

    overall = humans
    outside = group(OUTSIDE)
    newcomer = group(NEWCOMER)
    core = group(CORE)
    unknown = [item for item in humans if association(item) not in OUTSIDE | CORE]
    return {
        "population": population(items),
        "overall_merged": ratio(sum(merged(item) for item in overall), len(overall)),
        "outside_merged": ratio(sum(merged(item) for item in outside), len(outside)),
        "newcomer_merged": ratio(sum(merged(item) for item in newcomer), len(newcomer)),
        "core_merged": ratio(sum(merged(item) for item in core), len(core)),
        "unknown_count": len(unknown),
    }


def open_pr_metrics(items: list[dict[str, Any]], now: datetime) -> dict[str, Any]:
    humans = [item for item in items if not is_bot(item)]

    def age_days(item: dict[str, Any]) -> int:
        created = datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
        return max(0, (now - created).days)

    return {
        "population": population(items),
        "drafts": sum(bool(item.get("draft")) for item in humans),
        "older_than_30_days": sum(age_days(item) > 30 for item in humans),
        "older_than_90_days": sum(age_days(item) > 90 for item in humans),
        "oldest_human_pr_days": max((age_days(item) for item in humans), default=None),
    }


def pr_record(item: dict[str, Any]) -> dict[str, Any]:
    pull_request = item.get("pull_request") or {}
    return {
        "number": item.get("number"),
        "title": item.get("title"),
        "html_url": item.get("html_url"),
        "author": (item.get("user") or {}).get("login"),
        "author_type": (item.get("user") or {}).get("type"),
        "author_association": association(item),
        "draft": item.get("draft"),
        "created_at": item.get("created_at"),
        "closed_at": item.get("closed_at"),
        "merged_at": pull_request.get("merged_at"),
    }


def commit_activity(github: GitHub, repo: str) -> dict[str, Any]:
    for attempt in range(3):
        status, data, _ = github.get(f"repos/{repo}/stats/commit_activity", allowed={202, 204})
        if status == 200 and isinstance(data, list):
            totals = [int(week.get("total", 0)) for week in data]
            return {
                "available": True,
                "weeks": len(totals),
                "weeks_with_commits": sum(total > 0 for total in totals),
                "commits": sum(totals),
                "last_8_weeks": totals[-8:],
            }
        if status == 202 and attempt < 2:
            time.sleep(2**attempt)
            continue
        return {"available": False, "status": status}
    return {"available": False, "status": 202}


def collect(args: argparse.Namespace) -> dict[str, Any]:
    requested_repo = normalize_repo(args.repository)
    github = GitHub(discover_token())
    status, metadata, _ = github.get(f"repos/{requested_repo}")
    if status != 200 or not isinstance(metadata, dict):
        raise CollectionError("repository metadata was unavailable")
    repo = str(metadata["full_name"])
    now = datetime.now(timezone.utc)
    end = datetime.combine(now.date(), datetime.min.time(), tzinfo=timezone.utc) - timedelta(seconds=1)
    start = end - timedelta(days=args.days) + timedelta(seconds=1)

    _, languages, _ = github.get(f"repos/{repo}/languages")
    _, community, _ = github.get(f"repos/{repo}/community/profile", allowed={404})
    releases, releases_truncated = github.paginate(
        f"repos/{repo}/releases", max_pages=1
    )
    contributors, contributors_truncated = github.paginate(
        f"repos/{repo}/contributors", max_pages=args.max_contributor_pages
    )
    open_prs, open_prs_truncated = github.paginate(
        f"repos/{repo}/pulls",
        {"state": "open", "sort": "created", "direction": "asc"},
        max_pages=args.max_open_pr_pages,
    )
    open_search = github.search(f"repo:{repo} is:pr is:open")
    open_issues = github.search(f"repo:{repo} is:issue is:open")
    closed_prs, closed_integrity = collect_closed(github, repo, start, end)
    commits = commit_activity(github, repo)

    human_contributors = [item for item in contributors if item.get("type") != "Bot"]
    contributions = [int(item.get("contributions", 0)) for item in human_contributors]
    total_contributions = sum(contributions)

    return {
        "schema_version": 1,
        "collected_at": iso(now),
        "authenticated": bool(github.token),
        "api_requests": github.requests,
        "requested_repository": requested_repo,
        "canonical_repository": repo,
        "window": {
            "completed_utc_days": args.days,
            "start_inclusive": iso(start),
            "end_inclusive": iso(end),
        },
        "repository": {
            "html_url": metadata.get("html_url"),
            "description": metadata.get("description"),
            "archived": metadata.get("archived"),
            "fork": metadata.get("fork"),
            "default_branch": metadata.get("default_branch"),
            "license": (metadata.get("license") or {}).get("spdx_id"),
            "stars": metadata.get("stargazers_count"),
            "forks": metadata.get("forks_count"),
            "created_at": metadata.get("created_at"),
            "pushed_at": metadata.get("pushed_at"),
            "languages_bytes": languages or {},
            "community_profile": community,
        },
        "activity": {
            "commit_activity": commits,
            "recent_releases": [
                {
                    "tag_name": item.get("tag_name"),
                    "published_at": item.get("published_at"),
                    "html_url": item.get("html_url"),
                }
                for item in releases[:30]
            ],
            "releases_truncated": releases_truncated,
            "lifetime_contribution_concentration": {
                "contributors_collected": len(human_contributors),
                "pages_truncated": contributors_truncated,
                "top_contributor_share_percent": round(
                    max(contributions, default=0) / total_contributions * 100, 1
                )
                if total_contributions
                else None,
            },
        },
        "open_pull_requests": {
            "exact_total": int(open_search["total_count"]),
            "search_incomplete": bool(open_search.get("incomplete_results")),
            "items_collected": len(open_prs),
            "pages_truncated": open_prs_truncated,
            "metrics": open_pr_metrics(open_prs, now),
            "records": [pr_record(item) for item in open_prs],
        },
        "closed_pull_requests": {
            "integrity": closed_integrity,
            "outcomes": closed_outcomes(closed_prs),
            "records": [pr_record(item) for item in closed_prs],
        },
        "issues": {
            "exact_open_total": int(open_issues["total_count"]),
            "search_incomplete": bool(open_issues.get("incomplete_results")),
        },
        "sources": {
            "repository": metadata.get("html_url"),
            "pull_requests": f"https://github.com/{repo}/pulls",
            "issues": f"https://github.com/{repo}/issues",
            "releases": f"https://github.com/{repo}/releases",
            "open_pr_search": f"https://github.com/{repo}/pulls?q=is%3Apr+is%3Aopen",
            "open_issue_search": f"https://github.com/{repo}/issues?q=is%3Aissue+is%3Aopen",
            "closed_window_search": "https://github.com/"
            f"{repo}/pulls?q=is%3Apr+is%3Aclosed+closed%3A{urllib.parse.quote(iso(start))}"
            f"..{urllib.parse.quote(iso(end))}",
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", help="OWNER/REPO or github.com repository URL")
    parser.add_argument("--days", type=int, default=14, choices=range(1, 366), metavar="1..365")
    parser.add_argument("--max-open-pr-pages", type=int, default=20)
    parser.add_argument("--max-contributor-pages", type=int, default=10)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--force", action="store_true", help="overwrite an existing output file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        evidence = collect(args)
        rendered = json.dumps(evidence, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            if args.output.exists() and not args.force:
                raise CollectionError(f"output exists: {args.output}; pass --force to replace it")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"wrote {args.output}")
        else:
            sys.stdout.write(rendered)
        if not evidence["closed_pull_requests"]["integrity"]["complete"]:
            print("warning: closed-PR population failed its completeness check", file=sys.stderr)
            return 2
        return 0
    except (CollectionError, OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
