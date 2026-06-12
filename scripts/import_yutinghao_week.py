#!/usr/bin/env python3
"""Import this week's 游庭皓 YouTube captions into Stockhomes reports."""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import subprocess
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

CHANNEL_ID = "UC0lbAQVpenvfA2QqzsRtL_g"
CHANNEL_NAME = "游庭皓的財經皓角"
ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "yutinghao"
RAW_DIR = ROOT / "tmp" / "yutinghao-captions"

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}


def today_taipei() -> dt.date:
    return dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).date()


def week_start(day: dt.date) -> dt.date:
    return day - dt.timedelta(days=day.weekday())


def fetch_rss() -> list[dict]:
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
    data = urllib.request.urlopen(url, timeout=30).read()
    root = ET.fromstring(data)
    rows = []
    for entry in root.findall("atom:entry", NS):
        published = entry.findtext("atom:published", namespaces=NS)
        title = entry.findtext("atom:title", namespaces=NS)
        video_id = entry.findtext("yt:videoId", namespaces=NS)
        link = entry.find("atom:link", NS)
        if not published or not title or not video_id or link is None:
            continue
        published_dt = dt.datetime.fromisoformat(published.replace("Z", "+00:00"))
        rows.append(
            {
                "title": title,
                "video_id": video_id,
                "published": published_dt,
                "url": link.attrib["href"],
            }
        )
    return rows


def dump_ytdlp(url: str) -> dict:
    cmd = ["uvx", "--from", "yt-dlp", "yt-dlp", "--skip-download", "--dump-json", url]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    return json.loads(proc.stdout)


def best_subtitle(info: dict) -> tuple[str, str]:
    preferred_langs = ["zh-TW", "zh-Hant", "zh-Hans", "zh", "en"]
    subtitles = info.get("subtitles") or {}
    automatic = info.get("automatic_captions") or {}
    for source in (subtitles, automatic):
        for lang in preferred_langs:
            entries = source.get(lang) or []
            for ext in ("json3", "vtt", "srv3", "srt"):
                for item in entries:
                    if item.get("ext") == ext:
                        return lang, item["url"]
    raise RuntimeError(f"No usable subtitles found for {info.get('id')}")


def fetch_json3(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore"))


def fmt_ts(ms: int) -> str:
    total = round(ms / 1000)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def text_from_event(event: dict) -> str:
    text = "".join(seg.get("utf8", "") for seg in event.get("segs", []))
    text = html.unescape(text).replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def events_from_json3(data: dict) -> list[dict]:
    rows = []
    for event in data.get("events", []):
        text = text_from_event(event)
        if not text:
            continue
        if text in {"♪", "[音樂]", "[Music]"}:
            continue
        rows.append(
            {
                "start_ms": int(event.get("tStartMs", 0)),
                "duration_ms": int(event.get("dDurationMs", 0)),
                "text": text,
            }
        )
    return rows


def events_from_whisper_cache(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for segment in data.get("segments", []):
        text = re.sub(r"\s+", " ", str(segment.get("text", ""))).strip()
        if not text:
            continue
        start = float(segment.get("start", 0))
        end = float(segment.get("end", start))
        rows.append(
            {
                "start_ms": int(start * 1000),
                "duration_ms": max(0, int((end - start) * 1000)),
                "text": text,
            }
        )
    return rows


def transcribe_with_whisper(item: dict) -> tuple[str, list[dict]]:
    """Fallback for videos without YouTube captions."""
    whisper_cache = RAW_DIR / f"{item['video_id']}.whisper.json"
    if whisper_cache.exists():
        return "whisper-small-zh", events_from_whisper_cache(whisper_cache)

    audio_dir = ROOT / "tmp" / "yutinghao-audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(audio_dir / "%(id)s.%(ext)s")
    cmd = [
        "uvx",
        "--from",
        "yt-dlp",
        "yt-dlp",
        "-f",
        "ba/bestaudio",
        "-x",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "5",
        "-o",
        output_template,
        item["url"],
    ]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip())
    audio_path = audio_dir / f"{item['video_id']}.mp3"
    if not audio_path.exists():
        matches = list(audio_dir.glob(f"{item['video_id']}.*"))
        if not matches:
            raise RuntimeError(f"Downloaded audio not found for {item['video_id']}")
        audio_path = matches[0]

    from faster_whisper import WhisperModel

    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(audio_path), language="zh", beam_size=1, vad_filter=True, word_timestamps=False)
    rows = []
    for segment in segments:
        rows.append({"start": segment.start, "end": segment.end, "text": segment.text.strip()})
    whisper_cache.write_text(
        json.dumps({"language": info.language, "duration": info.duration, "segments": rows}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return "whisper-small-zh", events_from_whisper_cache(whisper_cache)


def yaml_quote(value: str) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def safe_filename(date_text: str, video_id: str) -> str:
    safe_id = video_id.replace("-", "m").replace("_", "u")
    return f"yutinghao-{date_text}-{safe_id}.md"


def description(title: str, events: list[dict]) -> str:
    body = " ".join(row["text"] for row in events[:12])
    desc = f"YouTube 字幕轉錄：{title}。{body}".strip()
    return desc[:170]


def episode_kind(title: str) -> str:
    if "早晨財經速解讀" in title:
        return "早晨財經速解讀"
    if "市場觀察" in title:
        return "市場觀察"
    return "游庭皓"


def markdown_for(item: dict, lang: str, events: list[dict]) -> str:
    published_tw = item["published"].astimezone(dt.timezone(dt.timedelta(hours=8)))
    date_text = published_tw.date().isoformat()
    title = item["title"]
    video_id = item["video_id"]
    kind = episode_kind(title)
    tags = ["游庭皓", kind, "逐字稿", "transcript"]
    aliases = ["游庭浩", "游庭皓的財經皓角", "早晨財經", video_id]
    keywords = [title, "YouTube 字幕", "台股", "美股", "總經", "市場觀察"]

    lines: list[str] = []
    lines.append("---")
    lines.append(f"title: {yaml_quote('游庭皓｜' + title)}")
    lines.append(f"date: {yaml_quote(date_text)}")
    lines.append("category: yutinghao")
    lines.append("tags:")
    for tag in tags:
        lines.append(f"- {yaml_quote(tag)}")
    lines.append(f"description: {yaml_quote(description(title, events))}")
    lines.append(f"source_url: {yaml_quote(item['url'])}")
    lines.append(f"video_id: {yaml_quote(video_id)}")
    lines.append(f"caption_language: {yaml_quote(lang)}")
    lines.append("aliases:")
    for alias in aliases:
        lines.append(f"- {yaml_quote(alias)}")
    lines.append("keywords:")
    for kw in keywords:
        lines.append(f"- {yaml_quote(kw)}")
    lines.append("---")
    lines.append("")
    lines.append(f"# 游庭皓｜{title}")
    lines.append("")
    lines.append(f"> 來源：{CHANNEL_NAME} YouTube 字幕")
    lines.append(f"> YouTube：[{item['url']}]({item['url']})")
    lines.append(f"> 影片 ID：`{video_id}`")
    lines.append(f"> 發布時間：{published_tw.strftime('%Y-%m-%d %H:%M')}（台北時間）")
    lines.append(f"> 字幕語言：`{lang}`")
    lines.append("> 注意：本文由 YouTube 字幕整理，未人工逐字校對；可能仍有斷句或同音字錯誤。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("[[toc]]")
    lines.append("")
    lines.append("## 逐字稿")
    lines.append("")

    current_bucket = None
    bucket_lines: list[str] = []
    bucket_start = None

    def flush() -> None:
        nonlocal bucket_lines, bucket_start
        if not bucket_lines:
            return
        lines.append(f"### {fmt_ts(bucket_start or 0)}")
        lines.append("")
        lines.extend(bucket_lines)
        lines.append("")
        bucket_lines = []
        bucket_start = None

    for row in events:
        bucket = row["start_ms"] // 120_000
        if current_bucket is None:
            current_bucket = bucket
            bucket_start = row["start_ms"]
        elif bucket != current_bucket:
            flush()
            current_bucket = bucket
            bucket_start = row["start_ms"]
        bucket_lines.append(row["text"])
    flush()
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--today", default=today_taipei().isoformat(), help="Taipei date used to pick the week")
    parser.add_argument("--since", default=None, help="Inclusive YYYY-MM-DD date override")
    parser.add_argument("--until", default=None, help="Inclusive YYYY-MM-DD date override")
    args = parser.parse_args(argv)

    today = dt.date.fromisoformat(args.today)
    since = dt.date.fromisoformat(args.since) if args.since else week_start(today)
    until = dt.date.fromisoformat(args.until) if args.until else today

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    rss_items = fetch_rss()
    selected = []
    for item in rss_items:
        local_date = item["published"].astimezone(dt.timezone(dt.timedelta(hours=8))).date()
        if since <= local_date <= until:
            selected.append(item)
    selected.sort(key=lambda row: row["published"])

    if not selected:
        print(f"No videos found from {since} to {until}")
        return 1

    print(f"Importing {len(selected)} videos from {since} to {until}")
    for item in selected:
        local_date = item["published"].astimezone(dt.timezone(dt.timedelta(hours=8))).date().isoformat()
        print(f"- {local_date} {item['video_id']} {item['title']}")
        info = dump_ytdlp(item["url"])
        try:
            lang, sub_url = best_subtitle(info)
            data = fetch_json3(sub_url)
            raw_path = RAW_DIR / f"{item['video_id']}.json"
            raw_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            events = events_from_json3(data)
        except RuntimeError as exc:
            print(f"  no usable YouTube subtitles ({exc}); falling back to Whisper ASR")
            lang, events = transcribe_with_whisper(item)
        if not events:
            raise RuntimeError(f"No caption events extracted for {item['video_id']}")
        md = markdown_for(item, lang, events)
        out = REPORT_DIR / safe_filename(local_date, item["video_id"])
        out.write_text(md, encoding="utf-8")
        print(f"  wrote {out.relative_to(ROOT)} ({len(events)} caption rows)")
        time.sleep(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
