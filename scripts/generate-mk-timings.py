#!/usr/bin/env python3
"""Generate section-level podcast timing sidecars for Stockhomes MK reports.

This does not download or serve audio. It keeps the SoundOn `audio_url` from
report frontmatter and writes small timestamp JSON files under data/mk-timings/.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from statistics import median

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = ROOT / "reports" / "mk"
TIMINGS_DIR = ROOT / "data" / "mk-timings"
GOOAYE_RAW_DIR = Path("/home/fc/foodmo/gooaye/transcripts/raw")

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
REPORT_RE = re.compile(r"gooaye-ep(\d{4})\.md$")


@dataclass
class Section:
    heading: str
    text: str


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    return re.sub(r"[\s\W_]+", "", text, flags=re.U)


def parse_markdown(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    match = FRONT_RE.match(raw)
    if not match:
        return {}, raw
    front = yaml.safe_load(match.group(1)) or {}
    return front, match.group(2)


def extract_sections(body: str) -> list[Section]:
    sections: list[Section] = []
    current_heading: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_heading, current_lines
        if current_heading is None:
            return
        text = "\n".join(current_lines).strip()
        sections.append(Section(current_heading, text))
        current_heading = None
        current_lines = []

    for line in body.splitlines():
        h2 = re.match(r"^##\s+(.+?)\s*$", line)
        if h2:
            flush()
            current_heading = h2.group(1).strip()
            current_lines = []
            continue
        if current_heading is not None:
            if line.startswith("# "):
                continue
            current_lines.append(line)
    flush()
    excluded_headings = {"註記", "附註", "備註", "資料來源", "來源", "參考資料", "references"}
    return [
        s for s in sections
        if len(normalize(s.text)) >= 12 and s.heading.strip().lower() not in excluded_headings
    ]


def load_raw(ep: int) -> tuple[float, str, list[tuple[int, int, float, float]]]:
    path = GOOAYE_RAW_DIR / f"EP{ep:04d}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    duration = float(data.get("duration") or 0)
    parts: list[str] = []
    positions: list[tuple[int, int, float, float]] = []
    cursor = 0
    for segment in data.get("segments", []):
        text = normalize(segment.get("text", ""))
        if not text:
            continue
        start = cursor
        parts.append(text)
        cursor += len(text)
        end = cursor
        positions.append((start, end, float(segment["start"]), float(segment["end"])))
        duration = max(duration, float(segment["end"]))
    return duration, "".join(parts), positions


def time_at_char(char_index: int, positions: list[tuple[int, int, float, float]], fallback: float) -> float:
    lo, hi = 0, len(positions) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        start, end, t_start, _t_end = positions[mid]
        if char_index < start:
            hi = mid - 1
        elif char_index >= end:
            lo = mid + 1
        else:
            return t_start
    if lo < len(positions):
        return positions[lo][2]
    return fallback


def best_match_char(raw_text: str, query: str, search_start: int, search_end: int) -> tuple[float, int]:
    qlen = max(1, len(query))
    search_end = min(search_end, len(raw_text))
    if search_start >= search_end:
        return 0.0, min(search_start, len(raw_text) - 1)

    # A cheap exact-ish shortcut helps for lightly corrected transcripts.
    exact = raw_text.find(query[: min(32, qlen)], search_start, search_end)
    if exact != -1:
        score = SequenceMatcher(None, query, raw_text[exact : exact + qlen]).ratio()
        if score >= 0.86:
            return score, exact

    best_score = -1.0
    best_char = search_start
    # Step by normalized characters, then refine around the best candidate.
    for char in range(search_start, search_end, 5):
        score = SequenceMatcher(None, query, raw_text[char : char + qlen]).ratio()
        if score > best_score:
            best_score = score
            best_char = char
        if score >= 0.93:
            break

    refine_start = max(search_start, best_char - 35)
    refine_end = min(search_end, best_char + 36)
    for char in range(refine_start, refine_end):
        score = SequenceMatcher(None, query, raw_text[char : char + qlen]).ratio()
        if score > best_score:
            best_score = score
            best_char = char
    return max(0.0, best_score), best_char


def align_sections(ep: int, sections: list[Section], duration: float, raw_text: str, positions: list[tuple[int, int, float, float]]) -> list[dict]:
    starts: list[dict] = []
    last_char = 0

    for idx, section in enumerate(sections):
        section_norm = normalize(section.text)
        query = section_norm[:90] or normalize(section.heading)
        if len(query) < 24:
            query = (section_norm + normalize(section.heading))[:80]

        search_start = max(0, last_char - 220)
        # Most sections are much shorter than 25k normalized chars; this wide window
        # allows drift while preventing accidental matches far later in the episode.
        search_end = len(raw_text) if idx == len(sections) - 1 else min(len(raw_text), search_start + 25000)
        score, char = best_match_char(raw_text, query, search_start, search_end)
        starts.append(
            {
                "heading": section.heading,
                "char": char,
                "start": round(time_at_char(char, positions, duration), 2),
                "confidence": round(score, 3),
            }
        )
        last_char = max(char + max(20, len(query)), last_char + 1)

    out: list[dict] = []
    for idx, item in enumerate(starts):
        end = starts[idx + 1]["start"] - 0.05 if idx + 1 < len(starts) else duration
        start = float(item["start"])
        out.append(
            {
                "id": f"ep{ep:04d}-s{idx + 1:02d}",
                "heading": item["heading"],
                "start": round(start, 2),
                "end": round(max(start, float(end)), 2),
                "confidence": item["confidence"],
            }
        )
    return out


def generate_episode(report_path: Path, overwrite: bool = True) -> dict:
    match = REPORT_RE.match(report_path.name)
    if not match:
        return {"status": "skip", "reason": "not a gooaye report", "path": str(report_path)}
    ep = int(match.group(1))

    front, body = parse_markdown(report_path)
    audio_url = str(front.get("audio_url") or "").strip()
    if not audio_url:
        return {"ep": ep, "status": "skip", "reason": "missing audio_url"}

    raw_path = GOOAYE_RAW_DIR / f"EP{ep:04d}.json"
    if not raw_path.exists():
        return {"ep": ep, "status": "skip", "reason": "missing raw json"}

    sections = extract_sections(body)
    if not sections:
        return {"ep": ep, "status": "skip", "reason": "no h2 sections"}

    out_path = TIMINGS_DIR / f"EP{ep:04d}.json"
    if out_path.exists() and not overwrite:
        return {"ep": ep, "status": "skip", "reason": "exists"}

    duration, raw_text, positions = load_raw(ep)
    segments = align_sections(ep, sections, duration, raw_text, positions)

    payload = {
        "ep": ep,
        "source": f"auto-aligned from {report_path.relative_to(ROOT)} and {raw_path}",
        "quality": "experimental section-level alignment; low-confidence segments need listening check",
        "audio_url": audio_url,
        "duration": round(duration, 2),
        "segments": segments,
    }
    TIMINGS_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    confidences = [s["confidence"] for s in segments]
    return {
        "ep": ep,
        "status": "written",
        "sections": len(segments),
        "min_confidence": min(confidences) if confidences else None,
        "median_confidence": median(confidences) if confidences else None,
        "path": str(out_path.relative_to(ROOT)),
    }


def report_paths(selected_eps: list[int] | None) -> list[Path]:
    if selected_eps:
        return [REPORTS_DIR / f"gooaye-ep{ep:04d}.md" for ep in selected_eps]
    return sorted(REPORTS_DIR.glob("gooaye-ep*.md"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ep", type=int, action="append", help="episode number to generate; repeatable")
    parser.add_argument("--all", action="store_true", help="generate for all MK reports")
    parser.add_argument("--no-overwrite", action="store_true", help="skip existing timing sidecars")
    args = parser.parse_args()

    if not args.all and not args.ep:
        parser.error("pass --all or --ep EP")

    results = []
    for path in report_paths(args.ep):
        if not path.exists():
            results.append({"status": "skip", "reason": "missing report", "path": str(path)})
            continue
        result = generate_episode(path, overwrite=not args.no_overwrite)
        results.append(result)
        if result.get("status") == "written":
            print(
                f"EP{result['ep']:04d}: wrote {result['sections']} segments "
                f"min={result['min_confidence']:.3f} median={result['median_confidence']:.3f}"
            )
        else:
            ep = result.get("ep", "????")
            print(f"EP{ep}: skip {result.get('reason')}")

    written = [r for r in results if r.get("status") == "written"]
    skipped = [r for r in results if r.get("status") != "written"]
    low = [r for r in written if r.get("min_confidence") is not None and r["min_confidence"] < 0.55]
    print(
        f"Done: written={len(written)}, skipped={len(skipped)}, "
        f"low_min_confidence_lt_0.55={len(low)}"
    )
    if low[:20]:
        print("Low confidence sample:", ", ".join(f"EP{r['ep']:04d}:{r['min_confidence']:.2f}" for r in low[:20]))


if __name__ == "__main__":
    main()
