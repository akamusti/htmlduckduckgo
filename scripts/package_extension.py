#!/usr/bin/env python3
"""Build a clean Chrome Web Store / unpacked-install ZIP."""

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "dist" / "htmlduckduckgo-chrome.zip"
FILES = (
    "manifest.json",
    "popup.html",
    "popup.css",
    "popup.js",
    "assets/icons/icon16.png",
    "assets/icons/icon48.png",
    "assets/icons/icon128.png",
)
SEARCH_URL = "https://html.duckduckgo.com/html/?q={searchTerms}"


def validate_manifest(manifest: dict) -> None:
    if manifest.get("manifest_version") != 3:
        raise ValueError("The extension must use Manifest V3.")

    provider = manifest.get("chrome_settings_overrides", {}).get("search_provider", {})
    if provider.get("search_url") != SEARCH_URL or provider.get("is_default") is not True:
        raise ValueError("The DuckDuckGo HTML default search provider is misconfigured.")

    if manifest.get("action", {}).get("default_popup") != "popup.html":
        raise ValueError("The search popup is not configured in the manifest.")

    if manifest.get("permissions") or manifest.get("host_permissions"):
        raise ValueError("This extension should not request browser or host permissions.")


def build() -> Path:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    validate_manifest(manifest)

    for relative_path in FILES:
        if not (ROOT / relative_path).is_file():
            raise FileNotFoundError(f"Required extension file is missing: {relative_path}")

    referenced_files = {
        manifest["action"]["default_popup"],
        *manifest["icons"].values(),
    }
    if not referenced_files.issubset(FILES):
        raise ValueError(f"Manifest references files missing from package: {referenced_files - set(FILES)}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for relative_path in FILES:
            info = ZipInfo(relative_path, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (ROOT / relative_path).read_bytes())

    with ZipFile(OUTPUT) as archive:
        packaged_files = set(archive.namelist())
        if packaged_files != set(FILES):
            raise ValueError(f"Unexpected release contents: {packaged_files ^ set(FILES)}")
        validate_manifest(json.loads(archive.read("manifest.json")))

    return OUTPUT


if __name__ == "__main__":
    print(f"Built {build().relative_to(ROOT)}")
