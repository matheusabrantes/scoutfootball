from __future__ import annotations

import argparse
import json
import http.client
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.services.providers.statsbomb_open import StatsBombOpenDataProvider  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a selected StatsBomb Open Data subset.")
    parser.add_argument("--competition-id", type=int, required=True)
    parser.add_argument("--season-id", type=int, required=True)
    parser.add_argument("--limit-matches", type=int)
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--force-refresh", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.full and args.limit_matches is None:
        args.limit_matches = 5
    provider = StatsBombOpenDataProvider()
    if args.force_refresh:
        _remove_cached_competition(provider.data_dir, args.competition_id, args.season_id)

    started = time.perf_counter()
    matches = provider.list_matches(args.competition_id, args.season_id)
    selected_matches = matches if args.full else matches[: args.limit_matches]
    downloaded = {"matches": 1, "events": 0, "lineups": 0, "three_sixty": 0}
    skipped = {"events": 0, "lineups": 0, "three_sixty": 0}
    failed: list[dict[str, str | int]] = []

    paths = provider.repository_paths()
    for index, match in enumerate(selected_matches, start=1):
        match_id = int(match["match_id"])
        print(f"[{index}/{len(selected_matches)}] match {match_id}", flush=True)
        for kind, repo_path, reader in (
            ("events", f"data/events/{match_id}.json", provider.read_events),
            ("lineups", f"data/lineups/{match_id}.json", provider.read_lineups),
            ("three_sixty", f"data/three-sixty/{match_id}.json", provider.read_three_sixty),
        ):
            if repo_path not in paths:
                continue
            cache_path = provider.data_dir / (
                f"three-sixty/{match_id}.json" if kind == "three_sixty" else f"{kind}/{match_id}.json"
            )
            if cache_path.exists() and not args.force_refresh:
                skipped[kind] += 1
                continue
            try:
                payload = _read_with_retry(reader, match_id)
                if not isinstance(payload, list):
                    raise ValueError(f"{kind} payload is not a JSON list")
                downloaded[kind] += 1
            except (
                HTTPError,
                URLError,
                TimeoutError,
                ValueError,
                json.JSONDecodeError,
                http.client.IncompleteRead,
            ) as exc:
                failed.append({"match_id": match_id, "kind": kind, "error": str(exc)})

    summary = {
        "competition_id": args.competition_id,
        "season_id": args.season_id,
        "repository_match_count": len(matches),
        "selected_match_count": len(selected_matches),
        "full": args.full,
        "downloaded": downloaded,
        "skipped": skipped,
        "failed": failed,
        "disk_usage": _directory_size(provider.data_dir),
        "processing_time_seconds": round(time.perf_counter() - started, 3),
    }
    output_path = provider.data_dir / "download_summary.json"
    output_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if failed else 0


def _read_with_retry(reader, match_id: int):
    last_error = None
    for attempt in range(3):
        try:
            return reader(match_id)
        except (HTTPError, URLError, TimeoutError, http.client.IncompleteRead) as exc:
            last_error = exc
            time.sleep(0.5 * (attempt + 1))
    if last_error:
        raise last_error
    raise RuntimeError("unreachable retry state")


def _remove_cached_competition(data_dir: Path, competition_id: int, season_id: int) -> None:
    match_cache = data_dir / "matches" / f"{competition_id}_{season_id}.json"
    if match_cache.exists():
        match_cache.unlink()


def _directory_size(path: Path) -> str:
    total = sum(item.stat().st_size for item in path.rglob("*") if item.is_file())
    if total < 1024 * 1024:
        return f"{round(total / 1024, 1)} KB"
    return f"{round(total / 1024 / 1024, 2)} MB"


if __name__ == "__main__":
    raise SystemExit(main())
