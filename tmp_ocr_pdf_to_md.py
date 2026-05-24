import re
import statistics
import sys
from pathlib import Path


DEPS_DIR = Path(r"C:\Users\Eu\AppData\Local\Temp\opencode\ocrdeps")
PDF_PATH = Path(r"D:\Obsidian\github_valut\Obsidian_vault\测试开发\笔记\AI测试\assets\AI项目\AI项目课堂笔记.pdf")
OUT_PATH = Path(r"D:\Obsidian\github_valut\Obsidian_vault\测试开发\笔记\AI测试\AI项目课堂笔记-纯文字版.md")


sys.path.insert(0, str(DEPS_DIR))
sys.stdout.reconfigure(encoding="utf-8")

import fitz  # type: ignore
from rapidocr_onnxruntime import RapidOCR  # type: ignore


def normalize_text(text: str) -> str:
    text = text.replace("\u3000", " ").strip()
    text = re.sub(r"\s+", " ", text)
    text = text.replace("（ ", "（").replace(" ）", "）")
    text = text.replace("[ ", "[").replace(" ]", "]")
    text = text.replace("( ", "(").replace(" )", ")")
    return text.strip()


def is_code_line(text: str) -> bool:
    plain = re.sub(r"^\d+\s*", "", text).strip()
    chinese_count = sum("\u4e00" <= ch <= "\u9fff" for ch in plain)
    english_count = sum("a" <= ch.lower() <= "z" for ch in plain)
    code_patterns = [
        r"^(from|import)\s+",
        r"^class\s+\w+",
        r"^def\s+\w+",
        r"^if\s+.*:",
        r"^elif\s+.*:",
        r"^else:",
        r"^try:",
        r"^except\b",
        r"^raise\b",
        r"^return\b",
        r"^print\(",
        r"^logger\.",
        r"^self\.",
        r"^connections\.",
        r"^utility\.",
        r"^FieldSchema\(",
        r"^CollectionSchema\(",
        r"^Collection\(",
        r"^SentenceTransformer\(",
        r"^[A-Z_]{2,}\s*=",
        r"^[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*['\"\[{(]",
        r"^#",
    ]
    if any(re.search(pattern, plain) for pattern in code_patterns):
        return True
    symbol_count = sum(plain.count(ch) for ch in "()[]{}=:_")
    return chinese_count == 0 and symbol_count >= 4 and english_count >= 6


def clean_bullet(text: str) -> str:
    return re.sub(r"^[·•●◦。oO]\s*", "", text).strip()


def heading_level(text: str, x: float, h: float, base_x: float, body_h: float, page_num: int) -> int:
    if page_num == 0 and text == "AI项目课堂笔记":
        return 1
    if re.match(r"^\d+\.\d+\.\d+(?![<>=])", text) and len(text) <= 32 and "：" not in text:
        return 4
    if re.match(r"^\d+\.\d+(?![<>=])", text) and len(text) <= 32 and "：" not in text:
        return 3
    if re.match(r"^\d+\.(?!\d)", text) and x <= base_x + 24 and len(text) <= 24 and "：" not in text:
        return 2
    if x <= base_x + 10 and h >= body_h * 1.25 and len(text) <= 24:
        return 2
    return 0


def should_skip(text: str, y: float, page_num: int) -> bool:
    if not text:
        return True
    # 跳过第一页顶部的页面 UI 文案，保留正文标题。
    if page_num == 0 and y < 110 and text in {"软件测试", "昨天修改", "AI速览试用"}:
        return True
    if page_num == 0 and "软件测试" in text and "昨天修改" in text:
        return True
    return False


def merge_row_text(items: list[dict]) -> str:
    items = sorted(items, key=lambda item: item["x"])
    parts: list[str] = []
    prev_right = None
    for item in items:
        text = item["text"]
        if not parts:
            parts.append(text)
        else:
            gap = item["x"] - (prev_right or item["x"])
            if gap > max(18, item["h"] * 0.6):
                parts.append(" ")
            parts.append(text)
        prev_right = item["x2"]
    return normalize_text("".join(parts))


def ocr_page(engine: RapidOCR, page: fitz.Page) -> list[dict]:
    pix = page.get_pixmap(dpi=180, alpha=False)
    result, _ = engine(pix.tobytes("png"))
    if not result:
        return []

    spans = []
    for item in result:
        points = item[0]
        text = normalize_text(item[1])
        if not text:
            continue
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        spans.append(
            {
                "x": min(xs),
                "y": min(ys),
                "x2": max(xs),
                "y2": max(ys),
                "h": max(ys) - min(ys),
                "text": text,
            }
        )

    spans.sort(key=lambda item: (item["y"], item["x"]))
    rows: list[list[dict]] = []
    current: list[dict] = []
    current_center = None

    for span in spans:
        center = (span["y"] + span["y2"]) / 2
        if not current:
            current = [span]
            current_center = center
            continue

        threshold = max(10, min(span["h"], current[-1]["h"]) * 0.65)
        if abs(center - (current_center or center)) <= threshold:
            current.append(span)
            current_center = statistics.mean([(item["y"] + item["y2"]) / 2 for item in current])
        else:
            rows.append(current)
            current = [span]
            current_center = center

    if current:
        rows.append(current)

    merged = []
    for row in rows:
        text = merge_row_text(row)
        if not text:
            continue
        merged.append(
            {
                "x": min(item["x"] for item in row),
                "y": min(item["y"] for item in row),
                "x2": max(item["x2"] for item in row),
                "h": max(item["h"] for item in row),
                "text": text,
            }
        )
    return merged


def render_markdown(lines: list[dict], page_num: int) -> list[str]:
    if not lines:
        return []

    body_candidates = [line["h"] for line in lines if 12 <= line["h"] <= 42]
    body_h = statistics.median(body_candidates) if body_candidates else 20
    base_candidates = [line["x"] for line in lines if line["y"] > 80 and line["x"] < 180]
    base_x = min(base_candidates) if base_candidates else min(line["x"] for line in lines)
    indent_unit = max(28, body_h * 1.5)

    output: list[str] = []
    in_code = False
    previous_kind = ""

    for line in lines:
        text = line["text"]
        if should_skip(text, line["y"], page_num):
            continue

        code_like = is_code_line(text)
        if code_like and not in_code:
            output.append("```python")
            in_code = True
        elif not code_like and in_code:
            output.append("```")
            output.append("")
            in_code = False

        if in_code:
            output.append(text)
            previous_kind = "code"
            continue

        level = heading_level(text, line["x"], line["h"], base_x, body_h, page_num)
        if level:
            if output and output[-1] != "":
                output.append("")
            output.append(f"{'#' * level} {text}")
            output.append("")
            previous_kind = "heading"
            continue

        indent_level = max(0, round((line["x"] - base_x) / indent_unit))
        indent = "    " * indent_level

        if re.match(r"^[·•●◦。oO]\s*", text):
            output.append(f"{indent}- {clean_bullet(text)}")
            previous_kind = "list"
            continue

        if re.match(r"^[a-zA-Z]\.", text):
            output.append(f"{indent}- {text}")
            previous_kind = "list"
            continue

        if re.match(r"^\d+\.", text) and indent_level > 0:
            output.append(f"{indent}{text}")
            previous_kind = "list"
            continue

        if previous_kind == "paragraph" and output and output[-1] and not output[-1].startswith(("#", "-", "```")):
            if not re.search(r"[。！？：；.?!:]$", output[-1]) and indent_level == 0:
                output[-1] += text
            else:
                output.append(f"{indent}{text}")
        else:
            output.append(f"{indent}{text}")
        previous_kind = "paragraph"

    if in_code:
        output.append("```")
        output.append("")

    while output and output[-1] == "":
        output.pop()
    return output


def main() -> None:
    engine = RapidOCR()
    doc = fitz.open(PDF_PATH)
    md_lines: list[str] = []

    for page_num, page in enumerate(doc):
        page_lines = ocr_page(engine, page)
        md_lines.extend(render_markdown(page_lines, page_num))
        md_lines.append("")

    content = "\n".join(md_lines).strip() + "\n"
    OUT_PATH.write_text(content, encoding="utf-8")
    print(f"已生成: {OUT_PATH}")


if __name__ == "__main__":
    main()
