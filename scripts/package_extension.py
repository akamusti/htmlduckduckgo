#!/usr/bin/env python3
"""Build platform-compatible Chrome extension ZIPs."""

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist" / "htmlduckduckgo-chrome.zip"
DESKTOP_OUTPUT = ROOT / "dist" / "htmlduckduckgo-chrome-desktop-search-override.zip"
FILES = (
    "manifest.json",
    "popup.html",
    "popup.css",
    "popup.js",
    "service-worker.js",
    "assets/icons/icon16.png",
    "assets/icons/icon48.png",
    "assets/icons/icon128.png",
)
SEARCH_URL = "https://html.duckduckgo.com/html/?q={searchTerms}"
SEARCH_PROVIDER = {
    "name": "DuckDuckGo HTML",
    "keyword": "duckduckgo.com",
    "search_url": SEARCH_URL,
    "encoding": "UTF-8",
    "is_default": True,
}


def validate_manifest(manifest: dict, *, desktop_override: bool) -> None:
    if manifest.get("manifest_version") != 3:
        raise ValueError("The extension must use Manifest V3.")

    if desktop_override:
        provider = manifest.get("chrome_settings_overrides", {}).get("search_provider", {})
        if provider != SEARCH_PROVIDER:
            raise ValueError("The DuckDuckGo HTML default search provider is misconfigured.")
    elif "chrome_settings_overrides" in manifest:
        raise ValueError("The portable package must not include platform-restricted settings overrides.")

    if manifest.get("action", {}).get("default_popup") != "popup.html":
        raise ValueError("The search popup is not configured in the manifest.")

    if manifest.get("omnibox", {}).get("keyword") != "ddg":
        raise ValueError("The portable DuckDuckGo omnibox keyword is misconfigured.")

    if manifest.get("background", {}).get("service_worker") != "service-worker.js":
        raise ValueError("The omnibox service worker is not configured in the manifest.")

    if manifest.get("permissions") or manifest.get("host_permissions"):
        raise ValueError("This extension should not request browser or host permissions.")


def _write_archive(output: Path, manifest: dict, files: tuple[str, ...]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for relative_path in files:
            info = ZipInfo(relative_path, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            contents = (
                json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
                if relative_path == "manifest.json"
                else (ROOT / relative_path).read_bytes()
            )
            archive.writestr(info, contents)

    with ZipFile(output) as archive:
        packaged_files = set(archive.namelist())
        if packaged_files != set(files):
            raise ValueError(f"Unexpected release contents: {packaged_files ^ set(files)}")
        validate_manifest(
            json.loads(archive.read("manifest.json")),
            desktop_override="chrome_settings_overrides" in manifest,
        )


def build() -> tuple[Path, Path]:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    validate_manifest(manifest, desktop_override=False)

    for relative_path in FILES:
        if not (ROOT / relative_path).is_file():
            raise FileNotFoundError(f"Required extension file is missing: {relative_path}")

    referenced_files = {
        manifest["action"]["default_popup"],
        *manifest["icons"].values(),
    }
    if not referenced_files.issubset(FILES):
        raise ValueError(f"Manifest references files missing from package: {referenced_files - set(FILES)}")

    desktop_manifest = {**manifest, "chrome_settings_overrides": {"search_provider": SEARCH_PROVIDER}}
    _write_archive(OUTPUT, manifest, FILES)
    _write_archive(DESKTOP_OUTPUT, desktop_manifest, FILES)
    return OUTPUT, DESKTOP_OUTPUT


if __name__ == "__main__":
    for package in build():
        print(f"Built {package.relative_to(ROOT)}")
