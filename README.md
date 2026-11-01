# DuckDuckGo HTML Search

Search via the extension popup in the Chrome toolbar or by typing `ddg` followed by <kbd>Tab</kbd> in the address bar. All searches open directly in DuckDuckGo's lightweight HTML interface.

---

## Downloads & Installation

> **Note:** Chrome's `chrome_settings_overrides` manifest key is only supported on **macOS** and **Windows**. Including this key on **Linux** or **ChromeOS** may cause installation to fail.

* **Linux / ChromeOS / Cross-Platform:** 
  Download and extract `htmlduckduckgo-chrome.zip`. Go to `chrome://extensions`, enable **Developer mode**, and select **Load unpacked** to load the extracted folder. Includes the extension popup and the `ddg` address bar shortcut.
* **macOS / Windows (Default Search Engine Override):** 
  Download and extract `htmlduckduckgo-chrome-desktop-search-override.zip` and load it using the same steps above. Chrome may ask for confirmation to override the default search engine.

### Setting Default Search Engine on Linux & ChromeOS

Due to Chrome platform restrictions, extensions cannot automatically modify default search engines via manifest settings on Linux or ChromeOS. To manually set DuckDuckGo HTML as default, navigate to `chrome://settings/searchEngines`, click **Add** under **Site search**, and enter:

* **Search engine:** `DuckDuckGo HTML`
* **Shortcut:** `duckduckgo.com`
* **URL:** `https://html.duckduckgo.com/html/?q=%s`

After adding, click the options menu next to the entry and select **Make default**.

---

## Build & Test

**Requirements:** Python 3 (no third-party packages required).

```bash
# Package the extension archives
python3 scripts/package_extension.py

# Run unit tests
python3 -m unittest discover -s tests
```

The build script generates two output packages:
1. A portable ZIP package without platform-restricted manifest keys.
2. A desktop ZIP package containing search engine overrides tailored for macOS and Windows.
