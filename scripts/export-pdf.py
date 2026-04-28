#!/usr/bin/env python3
from __future__ import annotations

import argparse
import functools
import html
import http.server
import json
import os
import pathlib
import re
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
from typing import Iterable


ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]


class StaticHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return

    def send_head(self):
        path = pathlib.Path(self.translate_path(self.path))
        if path.is_dir() and (path / "index.html").exists():
            self.path = self.path.rstrip("/") + "/index.html"
        elif not path.exists() and "." not in pathlib.PurePosixPath(self.path).name:
            fallback = pathlib.Path(self.directory) / self.path.strip("/") / "index.html"
            if fallback.exists():
                self.path = self.path.rstrip("/") + "/index.html"
        return super().send_head()


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def fail(message: str) -> None:
    print(f"[export-pdf] ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def log(message: str) -> None:
    print(f"[export-pdf] {message}")


def find_chrome(explicit: str | None = None, *, required: bool = False) -> str:
    if explicit:
        path = pathlib.Path(explicit)
        if path.exists():
            return str(path)
        found = shutil.which(explicit)
        if found:
            return found
        fail(f"Chrome executable not found: {explicit}")

    candidates = [
        os.environ.get("CHROME_BIN", ""),
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "microsoft-edge",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        found = shutil.which(candidate) if "/" not in candidate else candidate
        if found and pathlib.Path(found).exists():
            return str(found)
    if required:
        fail("Chrome, Chromium, or Edge is required for PDF export")
    return ""


def sidebars_doc_ids() -> list[str]:
    script = r"""
const sidebars = require(process.argv[1]);
const out = [];
const seen = new Set();
function add(id) {
  if (!id || seen.has(id)) return;
  seen.add(id);
  out.push(id);
}
function walk(item) {
  if (!item) return;
  if (typeof item === 'string') {
    add(item);
    return;
  }
  if (Array.isArray(item)) {
    item.forEach(walk);
    return;
  }
  if (item.type === 'doc') {
    add(item.id);
  }
  if (item.type === 'category') {
    if (item.link && item.link.type === 'doc') add(item.link.id);
    if (item.items) item.items.forEach(walk);
  }
}
add('intro');
Object.values(sidebars).forEach(walk);
console.log(JSON.stringify(out));
"""
    result = subprocess.run(
        ["node", "-e", script, str(ROOT_DIR / "sidebars.js")],
        check=True,
        cwd=str(ROOT_DIR),
        text=True,
        capture_output=True,
    )
    return list(json.loads(result.stdout))


def doc_file(build_dir: pathlib.Path, locale: str, doc_id: str) -> pathlib.Path:
    locale_root = build_dir if locale == "en" else build_dir / locale
    if doc_id == "intro":
        return locale_root / "index.html"
    if doc_id.endswith("/index"):
        return locale_root / doc_id.removesuffix("/index") / "index.html"
    return locale_root / doc_id / "index.html"


def extract_markdown(html_text: str, source: pathlib.Path) -> str:
    marker = 'class="theme-doc-markdown markdown"'
    marker_index = html_text.find(marker)
    if marker_index < 0:
        fail(f"Could not find Docusaurus markdown body in {source}")
    start = html_text.rfind("<div", 0, marker_index)
    end = html_text.find("<footer", marker_index)
    if start < 0 or end < 0 or end <= start:
        fail(f"Could not extract article body from {source}")
    return html_text[start:end]


def extract_title(article_html: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", article_html, flags=re.S)
    if not match:
        return "Untitled"
    text = re.sub(r"<[^>]+>", "", match.group(1))
    return html.unescape(" ".join(text.split()))


def build_print_html(
    *,
    build_dir: pathlib.Path,
    locale: str,
    doc_ids: Iterable[str],
) -> pathlib.Path:
    language_name = "English" if locale == "en" else "简体中文"
    title = "AtlasClaw Documentation" if locale == "en" else "AtlasClaw 文档"
    output_dir = build_dir / "__pdf"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"atlasclaw-doc-{locale}.html"

    articles: list[tuple[str, str]] = []
    for doc_id in doc_ids:
        path = doc_file(build_dir, locale, doc_id)
        if not path.exists():
            fail(f"Missing built doc page for {locale}: {doc_id} ({path})")
        body = extract_markdown(path.read_text(encoding="utf-8"), path)
        articles.append((extract_title(body), body))

    toc_items = "\n".join(
        f'<li><a href="#doc-{index}">{html.escape(page_title)}</a></li>'
        for index, (page_title, _) in enumerate(articles, start=1)
    )
    article_blocks = "\n".join(
        f'<section class="doc-page" id="doc-{index}">{body}</section>'
        for index, (_, body) in enumerate(articles, start=1)
    )

    output.write_text(
        f"""<!doctype html>
<html lang="{locale}">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)} PDF</title>
  <style>
    @page {{ size: A4; margin: 18mm 16mm; }}
    * {{ box-sizing: border-box; }}
    body {{
      color: #172033;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", "Helvetica Neue", Arial, sans-serif;
      font-size: 10.5pt;
      line-height: 1.55;
      margin: 0;
    }}
    .cover {{
      align-items: center;
      display: flex;
      flex-direction: column;
      justify-content: center;
      min-height: 230mm;
      page-break-after: always;
      text-align: center;
    }}
    .cover h1 {{ font-size: 34pt; margin: 0 0 12pt; }}
    .cover p {{ color: #526071; font-size: 13pt; margin: 0; }}
    .toc {{ page-break-after: always; }}
    .toc h1 {{ font-size: 22pt; margin-top: 0; }}
    .toc li {{ margin: 5pt 0; }}
    .toc a {{ color: #172033; text-decoration: none; }}
    .doc-page {{ page-break-before: always; }}
    .doc-page:first-of-type {{ page-break-before: auto; }}
    h1 {{ color: #0f172a; font-size: 22pt; margin: 0 0 14pt; }}
    h2 {{ border-bottom: 1px solid #d7dde8; color: #1e293b; font-size: 16pt; margin: 24pt 0 8pt; padding-bottom: 4pt; }}
    h3 {{ color: #334155; font-size: 13pt; margin: 18pt 0 6pt; }}
    h4 {{ color: #475569; font-size: 11.5pt; margin: 14pt 0 4pt; }}
    p {{ margin: 7pt 0; }}
    a {{ color: #0f5fcb; }}
    code {{
      background: #f2f5f9;
      border-radius: 3px;
      color: #9f1239;
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      font-size: 9.2pt;
      padding: 1px 3px;
    }}
    pre {{
      background: #f6f8fb;
      border: 1px solid #d9e0ea;
      border-radius: 6px;
      margin: 10pt 0;
      overflow-wrap: anywhere;
      padding: 9pt;
      white-space: pre-wrap;
    }}
    pre code {{ background: transparent; color: #172033; padding: 0; }}
    table {{ border-collapse: collapse; margin: 10pt 0 14pt; width: 100%; }}
    th, td {{ border: 1px solid #cbd5e1; padding: 6pt 7pt; text-align: left; vertical-align: top; }}
    th {{ background: #eef3f8; font-weight: 700; }}
    blockquote {{ border-left: 4px solid #cbd5e1; color: #475569; margin: 10pt 0; padding: 2pt 0 2pt 10pt; }}
    img {{ max-width: 100%; }}
    button, .hash-link, .theme-doc-breadcrumbs, .theme-doc-footer, .pagination-nav, .table-of-contents {{ display: none !important; }}
    .clean-btn, .buttonGroup__atx {{ display: none !important; }}
    svg {{ max-width: 1em; max-height: 1em; }}
  </style>
</head>
<body>
  <section class="cover">
    <h1>{html.escape(title)}</h1>
    <p>{html.escape(language_name)} PDF Export</p>
  </section>
  <section class="toc">
    <h1>Table of Contents</h1>
    <ol>
      {toc_items}
    </ol>
  </section>
  {article_blocks}
</body>
</html>
""",
        encoding="utf-8",
    )
    return output


def start_server(build_dir: pathlib.Path, port: int) -> ReusableTCPServer:
    handler = functools.partial(StaticHandler, directory=str(build_dir))
    server = ReusableTCPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def print_pdf_with_playwright(chrome: str, url: str, output_pdf: pathlib.Path) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return False

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        launch_args = {"headless": True}
        if chrome:
            launch_args["executable_path"] = chrome
        browser = playwright.chromium.launch(**launch_args)
        page = browser.new_page(viewport={"width": 1240, "height": 1754})
        page.goto(url, wait_until="networkidle", timeout=90_000)
        page.emulate_media(media="print")
        page.pdf(
            path=str(output_pdf),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
        )
        browser.close()
    return True


def print_pdf_with_chrome_cli(chrome: str, url: str, output_pdf: pathlib.Path) -> None:
    if not chrome:
        fail(
            "PDF export needs either Python Playwright or a Chrome/Chromium/Edge executable"
        )
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="atlasclaw-pdf-chrome-") as user_data_dir:
        command = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--disable-background-networking",
            "--disable-default-apps",
            "--disable-extensions",
            "--disable-sync",
            "--no-first-run",
            "--no-sandbox",
            f"--user-data-dir={user_data_dir}",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=1000",
            f"--print-to-pdf={output_pdf}",
            url,
        ]
        try:
            result = subprocess.run(command, text=True, capture_output=True, timeout=90)
        except subprocess.TimeoutExpired:
            result = subprocess.CompletedProcess(command, 124, "", "Chrome PDF export timed out")
        if result.returncode != 0:
            command[1] = "--headless"
            try:
                result = subprocess.run(command, text=True, capture_output=True, timeout=90)
            except subprocess.TimeoutExpired:
                result = subprocess.CompletedProcess(command, 124, "", "Chrome PDF export timed out")
    if result.returncode != 0:
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        fail(f"Chrome PDF export failed for {url}")


def print_pdf(chrome: str, url: str, output_pdf: pathlib.Path) -> None:
    if not print_pdf_with_playwright(chrome, url, output_pdf):
        print_pdf_with_chrome_cli(chrome, url, output_pdf)
    if not output_pdf.exists() or output_pdf.stat().st_size == 0:
        fail(f"PDF export did not write output: {output_pdf}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export AtlasClaw docs to static PDFs")
    parser.add_argument("--build-dir", default=str(ROOT_DIR / "build"))
    parser.add_argument("--output-dir", default=str(ROOT_DIR / "dist" / "pdf"))
    parser.add_argument("--port", type=int, default=18280)
    parser.add_argument("--chrome", default="")
    args = parser.parse_args()

    build_dir = pathlib.Path(args.build_dir).resolve()
    output_dir = pathlib.Path(args.output_dir).resolve()
    if not (build_dir / "index.html").exists():
        fail(f"Missing Docusaurus build directory: {build_dir}")

    chrome = find_chrome(args.chrome or None)
    doc_ids = sidebars_doc_ids()
    log(f"Using browser: {chrome}")
    log(f"Preparing {len(doc_ids)} docs per locale")

    en_html = build_print_html(build_dir=build_dir, locale="en", doc_ids=doc_ids)
    zh_html = build_print_html(build_dir=build_dir, locale="zh-CN", doc_ids=doc_ids)

    server = start_server(build_dir, args.port)
    time.sleep(0.2)
    try:
        print_pdf(
            chrome,
            f"http://127.0.0.1:{args.port}/__pdf/{en_html.name}",
            output_dir / "atlasclaw-doc-en.pdf",
        )
        print_pdf(
            chrome,
            f"http://127.0.0.1:{args.port}/__pdf/{zh_html.name}",
            output_dir / "atlasclaw-doc-zh-CN.pdf",
        )
    finally:
        server.shutdown()
        server.server_close()

    log(f"Wrote {output_dir / 'atlasclaw-doc-en.pdf'}")
    log(f"Wrote {output_dir / 'atlasclaw-doc-zh-CN.pdf'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
