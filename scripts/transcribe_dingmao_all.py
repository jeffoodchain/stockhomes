#!/usr/bin/env python3
"""Download and transcribe all 定錨產業筆記 podcast episodes from SoundOn RSS."""
from __future__ import annotations

import concurrent.futures
import datetime as dt
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path("/home/fc/foodmo/stockhomes")
REPORT_DIR = ROOT / "reports" / "investanchors"
AUDIO_DIR = ROOT / "tmp" / "investanchors-audio"
CACHE_DIR = ROOT / "tmp" / "investanchors-cache"
RSS_URL = "https://feeds.soundon.fm/podcasts/06e16cf5-5b45-4863-bcdf-9343aa584f73.xml"


def safe_filename(title: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff\-]", "_", title)
    s = re.sub(r"_+", "_", s).strip("_")[:80]
    return s


def fetch_rss() -> list[dict]:
    req = urllib.request.Request(RSS_URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    data = urllib.request.urlopen(req, timeout=60).read()
    root = ET.fromstring(data)
    ns = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}
    items = []
    for item in root.findall(".//item"):
        title = item.findtext("title", default="").strip()
        pub = item.findtext("pubDate", default="").strip()
        url = ""
        enc = item.find("enclosure")
        if enc is not None:
            url = enc.get("url", "")
        duration = item.findtext("itunes:duration", default="", namespaces=ns).strip()
        if title and url:
            items.append({"title": title, "pub": pub, "url": url, "duration": duration})
    return items


def download_episode(item: dict) -> Path:
    stem = safe_filename(item["title"])
    audio_path = AUDIO_DIR / f"{stem}.mp3"
    if audio_path.exists() and audio_path.stat().st_size > 100000:
        return audio_path
    print(f"[download] {item['title']}")
    req = urllib.request.Request(item["url"], headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        audio_path.write_bytes(resp.read())
    return audio_path


def transcribe_episode(item: dict, audio_path: Path) -> list[dict]:
    stem = safe_filename(item["title"])
    cache_path = CACHE_DIR / f"{stem}.whisper.json"
    if cache_path.exists():
        print(f"[cache] {item['title']}")
        return json.loads(cache_path.read_text(encoding="utf-8"))["segments"]

    print(f"[transcribe] {item['title']}")
    from faster_whisper import WhisperModel

    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(audio_path),
        language="zh",
        beam_size=1,
        vad_filter=True,
        word_timestamps=False,
    )
    rows = []
    for segment in segments:
        rows.append(
            {
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text.strip(),
            }
        )
    cache_path.write_text(
        json.dumps(
            {"language": info.language, "duration": info.duration, "segments": rows},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return rows


def fmt_ts(seconds: float) -> str:
    total = int(seconds)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def markdown_for(item: dict, segments: list[dict]) -> str:
    title = item["title"]
    pub_dt = None
    try:
        pub_dt = dt.datetime.strptime(item["pub"], "%a, %d %b %Y %H:%M:%S %Z")
        date_text = pub_dt.date().isoformat()
    except Exception:
        date_text = item["pub"]

    duration_sec = 0
    try:
        duration_sec = int(item["duration"])
    except Exception:
        if segments:
            duration_sec = int(segments[-1]["end"])

    safe = safe_filename(title)
    keywords = ["台股", "美股", "科技產業", "AI", "半導體", "PCB", "CPO"]

    def yaml_quote(value: str) -> str:
        return json.dumps(str(value), ensure_ascii=False)

    lines: list[str] = []
    lines.append("---")
    lines.append(f"title: {yaml_quote('定錨產業筆記｜' + title)}")
    lines.append(f"date: {yaml_quote(date_text)}")
    lines.append("category: investanchors")
    lines.append("tags:")
    for tag in ["investanchors", "科技產業趨勢領航者", "podcast", "逐字稿", "transcript"]:
        lines.append(f"- {yaml_quote(tag)}")
    lines.append(f"description: {yaml_quote('SoundOn Podcast 轉錄：' + title)}")
    lines.append(f"source_url: {yaml_quote(item['url'])}")
    lines.append(f"duration_seconds: {duration_sec}")
    lines.append("aliases:")
    lines.append(f"- {yaml_quote(title)}")
    lines.append("keywords:")
    for kw in keywords:
        lines.append(f"- {yaml_quote(kw)}")
    lines.append("---")
    lines.append("")
    lines.append(f"# 定錨產業筆記｜{title}")
    lines.append("")
    lines.append(f"> 來源：SoundOn Podcast RSS")
    lines.append(f"> 音檔：{item['url']}")
    lines.append(f"> 發布日期：{date_text}")
    lines.append(f"> 預估長度：{fmt_ts(duration_sec)}")
    lines.append("> 注意：本文由 faster-whisper small 自動轉錄，未人工逐字校對；可能仍有斷句或同音字錯誤。"
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("[[toc]]")
    lines.append("")

    # bucket into ~2-minute sections
    current_bucket: int | None = None
    bucket_lines: list[str] = []
    section_index = 0

    def flush() -> None:
        nonlocal bucket_lines, section_index, current_bucket
        if not bucket_lines:
            return
        start_text = fmt_ts(bucket_start)
        lines.append(f"## 段落 {section_index + 1}（{start_text}）")
        lines.append("")
        lines.extend(bucket_lines)
        lines.append("")
        bucket_lines = []
        current_bucket = None
        section_index += 1

    bucket_start = 0.0
    for seg in segments:
        bucket = int(seg["start"] // 120)
        text = f"[{fmt_ts(seg['start'])}] {seg['text']}"
        if current_bucket is None:
            current_bucket = bucket
            bucket_start = seg["start"]
            bucket_lines.append(text)
        elif bucket != current_bucket:
            flush()
            current_bucket = bucket
            bucket_start = seg["start"]
            bucket_lines.append(text)
        else:
            bucket_lines.append(text)
    flush()

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    items = fetch_rss()
    print(f"Found {len(items)} episodes")

    # download in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        audio_paths = list(executor.map(download_episode, items))

    # transcribe sequentially (CPU-heavy)
    for item, audio_path in zip(items, audio_paths):
        segments = transcribe_episode(item, audio_path)
        md = markdown_for(item, segments)
        out_path = REPORT_DIR / f"{safe_filename(item['title'])}.md"
        out_path.write_text(md, encoding="utf-8")
        print(f"[wrote] {out_path} ({len(segments)} segments)")

    print("All done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
