# Repository guide

- This repository contains a dependency-free Chrome Manifest V3 extension.
- `manifest.json` is the extension entry point; keep the permissions minimal.
- `popup.html`, `popup.css`, and `popup.js` implement the toolbar search popup.
- `assets/icons/` contains the raster icons referenced by the manifest.
- `dist/htmlduckduckgo-chrome.zip` is a generated release artifact. Build it from
  the allowlisted runtime files in `scripts/package_extension.py`, with
  `manifest.json` at the ZIP root; do not include repository metadata or
  documentation in the archive.
- Build and validate with `python3 scripts/package_extension.py`, then run
  `python3 -m unittest discover -s tests`.
- The default search provider is configured through
  `chrome_settings_overrides.search_provider`; Chrome asks the user to confirm
  this change when the extension is installed.
- Before calling any coding task complete, inspect the final changes for
  accidentally included credentials (API keys, access tokens, passwords,
  private keys), personal information, and other sensitive data. Do not commit
  real secrets. If runtime credentials are genuinely required, read them from
  environment variables, document the required names in a sanitized `.env.example`,
  and ensure local `.env` files are ignored. Never add an `.env` file merely
  because a credential-like word or public API endpoint appears in the code.
