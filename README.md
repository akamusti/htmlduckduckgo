# DuckDuckGo HTML Search

Search DuckDuckGo's lightweight HTML interface from the toolbar popup, or type `ddg`
followed by <kbd>Tab</kbd> in the address bar. You can also right-click selected text and
choose **Search "…" with DuckDuckGo HTML**.

---

## Downloads & installation

> **Note:** Chrome's `chrome_settings_overrides` manifest key is supported only on **macOS**
> and **Windows**. Including it on **Linux** or **ChromeOS** can make installation fail.

* **Linux / ChromeOS / cross-platform:**
  Download and extract `htmlduckduckgo-chrome.zip`. Open `chrome://extensions`, enable
  **Developer mode**, and choose **Load unpacked** to load the extracted folder. Includes the
  popup and the `ddg` address bar shortcut.
* **macOS / Windows (default search engine override):**
  Download and extract `htmlduckduckgo-chrome-desktop-search-override.zip` and install it the
  same way. Chrome may ask you to confirm the default search engine change.

## Making it the default search engine on Linux & ChromeOS

Chrome does not allow extensions to change the default search engine on Linux or ChromeOS, so
there is no way to do this automatically from the extension. Use the **Set as default search
engine** section in the popup for copyable values, or follow these steps:

1. Open `chrome://settings/searchEngines`.
2. Under **Site search**, choose **Add**.
3. Enter these values:
   * **Search engine:** `DuckDuckGo HTML`
   * **Shortcut:** `duckduckgo.com`
   * **URL:** `https://html.duckduckgo.com/html/?q=%s`
4. Save, then open the entry's options menu and select **Make default**.

### Fully automatic option for managed machines

On Linux, an administrator can preconfigure the search engine with Chrome policy. Create
`/etc/opt/chrome/policies/managed/duckduckgo-html.json` (for Chromium:
`/etc/chromium/policies/managed/`) containing:

```json
{
  "DefaultSearchProviderEnabled": true,
  "DefaultSearchProviderName": "DuckDuckGo HTML",
  "DefaultSearchProviderKeyword": "duckduckgo.com",
  "DefaultSearchProviderSearchURL": "https://html.duckduckgo.com/html/?q={searchTerms}",
  "DefaultSearchProviderEncodings": ["UTF-8"]
}
```

This requires root, applies to every profile of that browser install, and locks the setting
(the browser will show it as managed). On managed ChromeOS devices the equivalent setting lives
in the Google Admin console under **Devices → Chrome → Settings → Users & browsers → Search
provider**.

---

## Build & test

**Requirements:** Python 3 (no third-party packages required).

```bash
# Package the extension archives
python3 scripts/package_extension.py

# Run unit tests
python3 -m unittest discover -s tests
```

The build script generates two output packages:

1. A portable ZIP without platform-restricted manifest keys.
2. A desktop ZIP containing the search engine override for macOS and Windows.
