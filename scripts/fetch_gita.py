"""Fetch all 700 Bhagavad Gita verses from vedicscriptures.github.io and dump to JSON.

Output schema is quote-app friendly: one record per verse with English translations
from public-domain translators (Purohit + Sivananda).
"""

from __future__ import annotations

import io
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

API = "https://vedicscriptures.github.io/slok/{chapter}/{verse}"

# Standard verse counts per chapter (Gita = 700 verses total).
VERSES_PER_CHAPTER = {
    1: 47, 2: 72, 3: 43, 4: 42, 5: 29, 6: 47,
    7: 30, 8: 28, 9: 34, 10: 42, 11: 55, 12: 20,
    13: 35, 14: 27, 15: 20, 16: 24, 17: 28, 18: 78,
}

OUT_PATH = Path(r"C:/Users/chira/Desktop/bhagavad_gita.json")


def fetch_one(chapter: int, verse: int) -> dict | None:
    url = API.format(chapter=chapter, verse=verse)
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=20, headers={"Accept": "application/json"})
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
    return None


def normalize(record: dict) -> dict:
    purohit_block = record.get("purohit") or {}
    siva_block = record.get("siva") or {}
    return {
        "id": record.get("_id"),
        "chapter": record.get("chapter"),
        "verse": record.get("verse"),
        "sanskrit": record.get("slok"),
        "transliteration": record.get("transliteration"),
        "english": (purohit_block.get("et") or siva_block.get("et") or "").strip(),
        "english_alt": (siva_block.get("et") or "").strip() if purohit_block.get("et") else "",
        "translator": purohit_block.get("author") or siva_block.get("author"),
        "translator_alt": siva_block.get("author") if purohit_block.get("et") else None,
    }


def main() -> None:
    targets = [(c, v) for c, n in VERSES_PER_CHAPTER.items() for v in range(1, n + 1)]
    print(f"Fetching {len(targets)} verses across {len(VERSES_PER_CHAPTER)} chapters...")

    results: dict[tuple[int, int], dict] = {}
    failed: list[tuple[int, int]] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(fetch_one, c, v): (c, v) for c, v in targets}
        for i, fut in enumerate(as_completed(futures), 1):
            cv = futures[fut]
            data = fut.result()
            if data is None:
                failed.append(cv)
            else:
                results[cv] = normalize(data)
            if i % 50 == 0:
                print(f"  {i}/{len(targets)} done ({len(failed)} failed so far)")

    if failed:
        print(f"Retrying {len(failed)} failed verses sequentially...")
        for c, v in failed[:]:
            data = fetch_one(c, v)
            if data is not None:
                results[(c, v)] = normalize(data)
                failed.remove((c, v))

    ordered = [results[(c, v)] for c, v in targets if (c, v) in results]
    payload = {
        "source": "https://vedicscriptures.github.io/",
        "total_verses": len(ordered),
        "primary_translator": "Shri Purohit Swami (1935, public domain)",
        "fallback_translator": "Swami Sivananda",
        "verses": ordered,
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {OUT_PATH}")
    print(f"  {len(ordered)} of {len(targets)} verses captured")
    if failed:
        print(f"  STILL MISSING: {failed}")


if __name__ == "__main__":
    main()
