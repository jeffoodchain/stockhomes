#!/usr/bin/env python3
"""Reformat Invest Anchors transcripts into Stockhomes/MK-style articles.

The first pass produced timestamped ASR buckets. The desired Stockhomes style is
closer to the 股癌 pages: source block + meaningful `##` topic headings + prose
paragraphs, with no visible timestamps and no `## 段落 N` scaffolding.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports" / "investanchors"
TS_RE = re.compile(r"^\[(\d{2}:\d{2}:\d{2})\]\s*(.*)$")
FRONT_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)

# Topic plans are intentionally human-readable and conservative. They do not
# summarize away the transcript; they only provide article sections for the
# cleaned transcript paragraphs.
PLANS: dict[str, list[str]] = {
    "EP1-": [
        "開場：定錨產業筆記與 CES 2026 現場觀察",
        "NVIDIA Kyber Rack：從機櫃到交換器的規格升級",
        "BlueField、Grace CPU 與資料中心互聯",
        "高壓電源、MOSFET 與碳化矽機會",
        "SSD、NAND Flash 與記憶體供需",
        "CPO 交換器與矽光子供應鏈",
    ],
    "EP2-": [
        "開場：不對稱作戰與無人機升空",
        "烏俄戰爭後的無人機需求與戰術變化",
        "台灣軍工、飛彈與防空系統",
        "無人機零組件、自製率與供應鏈",
        "水面無人艇、海鯤號與國防採購",
        "投資視角：軍工題材的機會與限制",
    ],
    "EP3-": [
        "開場：2026 年全球經濟展望",
        "聯準會、利率與美元流動性",
        "大而美法案、財政赤字與美債殖利率",
        "日圓利差交易與全球資金流向",
        "中國、台灣與出口產業壓力",
        "信用循環、授信額度與風險控管",
        "結語：宏觀環境下的投資節奏",
    ],
    "EP4-": [
        "開場：2026 年產業趨勢總覽",
        "AI 伺服器與資料中心建置週期",
        "記憶體：DRAM、NAND Flash 與供需循環",
        "先進封裝、封測與台積電 CAPEX",
        "被動元件、功率元件與電源架構",
        "PCB、玻纖布與材料升級",
        "成熟製程、車用與邊緣應用",
        "投資節奏：題材、估值與風險",
    ],
    "EP5-": [
        "開場：先進封裝缺口外溢",
        "GPU、ASIC 與 Data Center CPU 的 CoWoS 需求",
        "台積電 CAPEX、先進製程與封裝產能分配",
        "日月光、Amkor 與專業代工廠角色",
        "設備、人力與良率：擴產真正卡點",
        "投資視角：先進封裝供應鏈怎麼看",
    ],
    "EP6-": [
        "開場：算力不缺，缺的是互聯",
        "Lumentum、Coherent 與雷射晶片供需",
        "AI 叢集互聯、光模組與 CPO 架構",
        "磷化銦基板、磊晶與上游瓶頸",
        "美中科技戰下的供應安全",
        "投資視角：光通訊景氣與風險",
    ],
    "EP7-": [
        "開場：AI 伺服器功耗與被動元件",
        "MLCC、鋁質電容與高容值需求",
        "800V、電源模組與功率元件升級",
        "供給端：日系廠、擴產與訂單出貨比",
        "會不會重演被動元件之亂",
        "投資視角：估值、景氣與風險控管",
    ],
    "EP8-": [
        "開場：成熟製程供需拐點",
        "轉單、漲價與滿載：需求端訊號",
        "8 吋、12 吋與晶圓代工產能",
        "功率元件、車用與工控需求",
        "台系廠商的競爭位置與風險",
        "投資視角：成熟製程循環怎麼追蹤",
    ],
    "EP9-": [
        "開場：GTC 與 NVIDIA 下一段成長曲線",
        "推論爆發 100 萬倍的意義",
        "Blackwell、Rubin 與資料中心升級",
        "BlueField、ConnectX-9 與網路互聯",
        "CPO、矽光與光互聯趨勢",
        "投資視角：AI 供應鏈從訓練走向推論",
    ],
    "EP10-": [
        "開場：OFC 現場與 CPO 真的來了嗎",
        "6.4T 平台、OCS 與交換器架構",
        "Lumentum、Coherent、VCSEL 與雷射方案",
        "Micro LED、Microlens 與光學封裝細節",
        "磷化銦、砷化鎵與矽光基底",
        "NPO、CPO 與可插拔式方案的取捨",
        "投資視角：光通訊供應鏈怎麼看",
    ],
    "EP11-": [
        "開場：定錨研究員的日常分享",
        "展會觀察：Touch Taiwan、COMPUTEX 與 SEMICON",
        "研究員工作流：找題目、寫報告與拜訪公司",
        "產業研究的樂趣與壓力",
        "投資人、法人與研究報告的互動",
        "閒聊：團隊文化、生活與下一步",
    ],
    "EP12-": [
        "開場：台積電 CAPEX 到上緣",
        "生成式 AI、代理式 AI 與軍備競賽",
        "法說會訊號：CAPEX、先進製程與先進封裝",
        "廠務、無塵室與機電工程機會",
        "設備、認列與訂單能見度",
        "風險：美伊衝突、黑天鵝與投資紀律",
    ],
    "EP13": [
        "開場：AI 伺服器推動 PCB 升級",
        "PCB、CCL 與玻纖布的供需瓶頸",
        "高層數、HDI 與厚大板製程挑戰",
        "鑽針、鑽孔、壓合與良率問題",
        "Low Dk、Low CTE、石英布與 HVLP 銅箔",
        "勝宏、臻鼎、定穎、滬士電與金像電擴產",
        "投資視角：材料端、板廠與設備端怎麼追蹤",
    ],
}

DESCRIPTION_OVERRIDES: dict[str, str] = {
    "EP1-": "CES 2026 現場觀察、NVIDIA Kyber Rack、CPO 交換器、高壓電源、NAND Flash 與矽光子供應鏈。",
    "EP2-": "不對稱作戰、烏俄戰爭後的無人機需求、台灣軍工供應鏈、防空飛彈與國防採購。",
    "EP3-": "2026 年全球經濟展望：聯準會、利率、美債、日圓利差交易、美元流動性與台灣出口產業。",
    "EP4-": "2026 年產業趨勢總覽：AI 伺服器、記憶體、先進封裝、被動元件、PCB 與成熟製程。",
    "EP5-": "先進封裝產能外溢，從 GPU、ASIC、Data Center CPU 到 CoWoS、專業代工廠與設備瓶頸。",
    "EP6-": "AI 算力互聯、光通訊、雷射晶片、磷化銦基板、CPO 架構與美中科技戰下的供應瓶頸。",
    "EP7-": "AI 伺服器功耗升級下的 MLCC、鋁質電容、功率元件與被動元件供需循環。",
    "EP8-": "成熟製程供需拐點，討論轉單、漲價、滿載、8 吋/12 吋晶圓代工與台系廠商機會。",
    "EP9-": "GTC 揭露 NVIDIA 推論成長曲線，從 Blackwell、Rubin、互聯、CPO 到 AI 供應鏈下一階段。",
    "EP10-": "OFC 現場觀察 CPO、OCS、6.4T 平台、雷射元件、矽光基底與可插拔式方案。",
    "EP11-": "定錨研究員日常分享：展會觀察、研究工作流、報告產製、法人互動與團隊閒聊。",
    "EP12-": "台積電 CAPEX 上緣下的先進製程、先進封裝、廠務工程、設備機會與投資風險。",
    "EP13": "AI 伺服器主板規格升級，拆解 PCB、CCL、玻纖布、石英布、銅箔、鑽針與板廠擴產瓶頸。",
}


def key_for(path: Path) -> str:
    for key in PLANS:
        if key in path.name:
            return key
    raise KeyError(path.name)


def clean_text(s: str) -> str:
    s = s.strip()
    # Tidy spacing introduced by ASR / previous glossary passes.
    s = re.sub(r"([A-Za-z0-9])\s+([A-Za-z0-9])", r"\1 \2", s)
    s = s.replace("Podcast", "Podcast")
    s = s.replace("PCB 的", "PCB 的")
    s = re.sub(r"\s+", " ", s)
    return s


def paragraphize(lines: list[str], max_chars: int = 260) -> list[str]:
    paragraphs: list[str] = []
    buf: list[str] = []
    size = 0
    for raw in lines:
        text = clean_text(raw)
        if not text:
            continue
        buf.append(text)
        size += len(text)
        # Keep paragraphs readable and 股癌-like: not timestamp fragments, not huge walls.
        if size >= max_chars or text.endswith(("。", "？", "！")) and size >= max_chars * 0.7:
            paragraphs.append("".join(buf))
            buf = []
            size = 0
    if buf:
        paragraphs.append("".join(buf))
    return paragraphs


def split_into_sections(lines: list[str], headings: list[str]) -> list[tuple[str, list[str]]]:
    n = len(lines)
    m = len(headings)
    sections: list[tuple[str, list[str]]] = []
    for i, heading in enumerate(headings):
        start = round(i * n / m)
        end = round((i + 1) * n / m)
        chunk = lines[start:end]
        sections.append((heading, paragraphize(chunk)))
    return sections


def update_description(frontmatter: str, desc: str) -> str:
    # YAML-safe because descriptions are plain Chinese/ASCII without quotes.
    return re.sub(r'^description:.*$', f'description: {desc}', frontmatter, flags=re.M)


def reformat(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    m = FRONT_RE.match(text)
    if not m:
        raise ValueError(f"No frontmatter: {path}")
    front = m.group(1)
    key = key_for(path)
    front = update_description(front, DESCRIPTION_OVERRIDES[key])

    title_match = re.search(r'^title:\s*"?(.*?)"?$', front, re.M)
    title = title_match.group(1) if title_match else path.stem
    title = title.strip('"')
    date = re.search(r'^date:\s*"?(.*?)"?$', front, re.M)
    duration = re.search(r'^duration_seconds:\s*(\d+)', front, re.M)
    source = re.search(r'^source_url:\s*"?(.*?)"?$', front, re.M)

    transcript_lines: list[str] = []
    for line in text.splitlines():
        mt = TS_RE.match(line)
        if mt:
            body = mt.group(2).strip()
            if body:
                transcript_lines.append(body)

    if not transcript_lines:
        # Already converted; leave unchanged.
        return False

    lines: list[str] = ["---", front.rstrip(), "---", "", f"# {title}", ""]
    lines.append("> 來源：SoundOn Podcast RSS")
    if source:
        url = source.group(1).strip('"')
        lines.append(f"> 音檔：{url}")
    if date:
        lines.append(f"> 發布日期：{date.group(1).strip(chr(34))}")
    if duration:
        sec = int(duration.group(1))
        h, r = divmod(sec, 3600)
        mi, se = divmod(r, 60)
        lines.append(f"> 預估長度：{h:02d}:{mi:02d}:{se:02d}")
    lines.append("> 整理：ASR 轉錄後依定錨/Stockhomes 風格整理為主題段落；已移除時間戳，保留逐字稿口語脈絡。")
    lines.extend(["", "---", ""])

    for heading, paragraphs in split_into_sections(transcript_lines, PLANS[key]):
        lines.append(f"## {heading}")
        lines.append("")
        lines.extend(paragraphs)
        lines.append("")

    new_text = "\n".join(lines).rstrip() + "\n"
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for path in sorted(REPORT_DIR.glob("*.md")):
        if reformat(path):
            changed += 1
            print(f"[reformatted] {path.name}")
        else:
            print(f"[unchanged] {path.name}")
    print(f"Reformatted {changed} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
