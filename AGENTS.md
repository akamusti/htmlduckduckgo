# Repository guide

- This repository contains a dependency-free Chrome Manifest V3 extension.
- `manifest.json` is the portable/Linux-safe extension entry point; keep the
  permissions minimal.
- `popup.html`, `popup.css`, and `popup.js` implement the toolbar search popup.
- `service-worker.js` handles the `ddg` omnibox keyword without host permissions.
- `assets/icons/` contains the raster icons referenced by the manifest.
- Chrome's `chrome_settings_overrides` manifest key is supported only on macOS
  and Windows. Keep it out of the portable manifest so the extension can load
  on Linux/ChromeOS. The packaging script adds it only to the explicitly
  desktop-only search override ZIP.
- Both release ZIPs are generated artifacts. Build them from the allowlisted
  runtime files in `scripts/package_extension.py`, with `manifest.json` at the
  ZIP root; do not include repository metadata or documentation in the archive.
- Build and validate with `python3 scripts/package_extension.py`, then run
  `python3 -m unittest discover -s tests`.
- Linux/ChromeOS users must add DuckDuckGo HTML as a search provider manually in
  Chrome settings to use it as their address-bar default.
- Before calling any coding task complete, inspect the final changes for
  accidentally included credentials (API keys, access tokens, passwords,
  private keys), personal information, and other sensitive data. Do not commit
  real secrets. If runtime credentials are genuinely required, read them from
  environment variables, document the required names in a sanitized `.env.example`,
  and ensure local `.env` files are ignored. Never add an `.env` file merely
  because a credential-like word or public API endpoint appears in the code.
