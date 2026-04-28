#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS_DIR="$ROOT_DIR/docs"
I18N_DOCS_DIR="$ROOT_DIR/i18n/zh-CN/docusaurus-plugin-content-docs/current"
DIST_DIR="${DIST_DIR:-$ROOT_DIR/dist}"
STAMP="${DOCS_EXPORT_STAMP:-$(date +%Y%m%d-%H%M%S)}"
EXPORT_NAME="atlasclaw-doc-$STAMP"
PACKAGE_DIR="$DIST_DIR/$EXPORT_NAME"
ARCHIVE="$DIST_DIR/$EXPORT_NAME.zip"
INCLUDE_PDF=false

for arg in "$@"; do
  case "$arg" in
    --pdf)
      INCLUDE_PDF=true
      ;;
    --no-pdf)
      INCLUDE_PDF=false
      ;;
    *)
      fail "Unknown argument: $arg"
      ;;
  esac
done

log() {
  printf '[export-docs] %s\n' "$1"
}

fail() {
  printf '[export-docs] ERROR: %s\n' "$1" >&2
  exit 1
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || fail "Missing required command: $1"
}

check_doc_paths() {
  log "Checking English and Chinese document path alignment"
  [[ -d "$DOCS_DIR" ]] || fail "Missing docs directory: $DOCS_DIR"
  [[ -d "$I18N_DOCS_DIR" ]] || fail "Missing Chinese docs directory: $I18N_DOCS_DIR"

  local en_paths zh_paths mismatch
  en_paths="$(mktemp)"
  zh_paths="$(mktemp)"

  find "$DOCS_DIR" -name '*.md' | sed "s#^$DOCS_DIR/##" | sort > "$en_paths"
  find "$I18N_DOCS_DIR" -name '*.md' | sed "s#^$I18N_DOCS_DIR/##" | sort > "$zh_paths"

  mismatch="$(comm -3 "$en_paths" "$zh_paths")"
  rm -f "$en_paths" "$zh_paths"
  if [[ -n "$mismatch" ]]; then
    printf '%s\n' "$mismatch" >&2
    fail "English and Chinese document trees are not aligned"
  fi
}

scan_sensitive_content() {
  log "Scanning source docs for local paths and obvious secret material"
  local pattern
  pattern='(/Users/|\.worktrees|admin/admin|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|BEGIN (RSA|OPENSSH|DSA|EC|PRIVATE) KEY)'

  if rg -n "$pattern" \
    "$ROOT_DIR/README.md" \
    "$ROOT_DIR/package.json" \
    "$ROOT_DIR/docusaurus.config.js" \
    "$ROOT_DIR/sidebars.js" \
    "$DOCS_DIR" \
    "$I18N_DOCS_DIR"; then
    fail "Sensitive or local-only content found in export source"
  fi
}

build_site() {
  log "Building Docusaurus site"
  (cd "$ROOT_DIR" && npm run build)
}

write_package_files() {
  log "Preparing offline package directory: $PACKAGE_DIR"
  rm -rf "$PACKAGE_DIR"
  mkdir -p "$PACKAGE_DIR"
  cp -R "$ROOT_DIR/build" "$PACKAGE_DIR/build"

  cat > "$PACKAGE_DIR/README.md" <<'EOF'
# AtlasClaw Docs Offline Package

Do not open `build/index.html` directly with `file://`. Docusaurus requires an
HTTP static server so its JavaScript, CSS, language routes, and navigation can
load correctly.

## macOS / Linux

```bash
./start.sh
```

On macOS, you can also double-click `start.command`.

## Windows

Double-click `start.bat`, or run:

```bat
start.bat
```

The scripts start a local static server and print the URL. The default URL is:

```text
http://127.0.0.1:8080/
```

Chinese documentation is available under:

```text
http://127.0.0.1:8080/zh-CN/
```

To use another port:

```bash
PORT=9000 ./start.sh
```
EOF

  cat > "$PACKAGE_DIR/start.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PORT="${PORT:-8080}"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  echo "Python 3 is required to serve this offline documentation package." >&2
  exit 1
fi

echo "Serving AtlasClaw Docs at http://127.0.0.1:${PORT}/"
echo "Press Ctrl+C to stop."
exec "$PYTHON_BIN" "$SCRIPT_DIR/tools/serve_docs.py" "$SCRIPT_DIR/build" "$PORT"
EOF

  cat > "$PACKAGE_DIR/start.command" <<'EOF'
#!/usr/bin/env bash
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"
exec ./start.sh
EOF

  cat > "$PACKAGE_DIR/start.bat" <<'EOF'
@echo off
setlocal
cd /d "%~dp0"
if "%PORT%"=="" set PORT=8080
where py >nul 2>nul
if %ERRORLEVEL%==0 (
  echo Serving AtlasClaw Docs at http://127.0.0.1:%PORT%/
  py -3 tools\serve_docs.py build %PORT%
  exit /b %ERRORLEVEL%
)
where python >nul 2>nul
if %ERRORLEVEL%==0 (
  echo Serving AtlasClaw Docs at http://127.0.0.1:%PORT%/
  python tools\serve_docs.py build %PORT%
  exit /b %ERRORLEVEL%
)
echo Python 3 is required to serve this offline documentation package.
exit /b 1
EOF

  mkdir -p "$PACKAGE_DIR/tools"
  cat > "$PACKAGE_DIR/tools/serve_docs.py" <<'PY'
#!/usr/bin/env python3
from __future__ import annotations

import functools
import http.server
import pathlib
import socketserver
import sys


class DocusaurusHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)
        requested = pathlib.Path(path)
        if requested.is_dir():
            index = requested / "index.html"
            if index.exists():
                self.path = self.path.rstrip("/") + "/index.html"
                return super().send_head()
        if not requested.exists() and "." not in pathlib.PurePosixPath(self.path).name:
            fallback = pathlib.Path(self.directory) / self.path.strip("/") / "index.html"
            if fallback.exists():
                self.path = self.path.rstrip("/") + "/index.html"
        return super().send_head()


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: serve_docs.py BUILD_DIR PORT", file=sys.stderr)
        return 2

    build_dir = pathlib.Path(sys.argv[1]).resolve()
    port = int(sys.argv[2])
    if not (build_dir / "index.html").exists():
        print(f"Missing Docusaurus build directory: {build_dir}", file=sys.stderr)
        return 1

    handler = functools.partial(DocusaurusHandler, directory=str(build_dir))
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        httpd.allow_reuse_address = True
        httpd.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
PY

  chmod +x "$PACKAGE_DIR/start.sh" "$PACKAGE_DIR/start.command" "$PACKAGE_DIR/tools/serve_docs.py"
}

write_pdf_files() {
  if [[ "$INCLUDE_PDF" != "true" ]]; then
    return
  fi
  log "Exporting static PDFs"
  python3 "$ROOT_DIR/scripts/export-pdf.py" \
    --build-dir "$ROOT_DIR/build" \
    --output-dir "$PACKAGE_DIR/pdf"
}

write_archive() {
  log "Creating archive: $ARCHIVE"
  mkdir -p "$DIST_DIR"
  rm -f "$ARCHIVE" "$ARCHIVE.sha256"

  if command -v zip >/dev/null 2>&1; then
    (cd "$DIST_DIR" && zip -qr "$ARCHIVE" "$EXPORT_NAME")
  elif command -v python3 >/dev/null 2>&1; then
    python3 - "$PACKAGE_DIR" "$ARCHIVE" "$EXPORT_NAME" <<'PY'
import pathlib
import sys
import zipfile

package_dir = pathlib.Path(sys.argv[1])
archive = pathlib.Path(sys.argv[2])
export_name = sys.argv[3]
with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for path in sorted(package_dir.rglob("*")):
        if path.is_file():
            zf.write(path, pathlib.Path(export_name) / path.relative_to(package_dir))
PY
  else
    fail "Need either zip or python3 to create the export archive"
  fi

  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$ARCHIVE" > "$ARCHIVE.sha256"
  elif command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$ARCHIVE" > "$ARCHIVE.sha256"
  fi
}

main() {
  require_cmd npm
  require_cmd rg
  check_doc_paths
  scan_sensitive_content
  build_site
  write_package_files
  write_pdf_files
  write_archive
  log "Export complete: $ARCHIVE"
  [[ -f "$ARCHIVE.sha256" ]] && log "Checksum: $ARCHIVE.sha256"
}

main "$@"
