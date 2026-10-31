import json
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent


class ExtensionPackageTests(unittest.TestCase):
    def test_manifest_configures_default_html_search_and_popup(self):
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["manifest_version"], 3)
        self.assertEqual(manifest["version"], "0.0.2")
        self.assertNotIn("chrome_settings_overrides", manifest)
        self.assertEqual(manifest["omnibox"]["keyword"], "ddg")
        self.assertEqual(manifest["background"]["service_worker"], "service-worker.js")
        self.assertEqual(manifest["action"]["default_popup"], "popup.html")
        self.assertNotIn("permissions", manifest)
        self.assertNotIn("host_permissions", manifest)

    def test_desktop_package_enables_default_html_search(self):
        archive_path = ROOT / "dist" / "htmlduckduckgo-chrome-desktop-search-override.zip"
        self.assertTrue(archive_path.is_file(), "Build the desktop release ZIP before running tests.")

        with ZipFile(archive_path) as archive:
            manifest = json.loads(archive.read("manifest.json"))
            provider = manifest["chrome_settings_overrides"]["search_provider"]
            self.assertTrue(provider["is_default"])
            self.assertEqual(
                provider["search_url"],
                "https://html.duckduckgo.com/html/?q={searchTerms}",
            )

    def test_omnibox_search_opens_duckduckgo_html(self):
        service_worker = (ROOT / "service-worker.js").read_text(encoding="utf-8")

        self.assertIn("chrome.omnibox.onInputEntered.addListener", service_worker)
        self.assertIn("encodeURIComponent(text)", service_worker)
        self.assertIn("https://html.duckduckgo.com/html/?q=", service_worker)

    def test_popup_submits_searches_to_html_endpoint(self):
        popup = (ROOT / "popup.html").read_text(encoding="utf-8")

        self.assertIn('action="https://html.duckduckgo.com/html/"', popup)
        self.assertIn('method="get"', popup)
        self.assertIn('name="q"', popup)
        self.assertIn('target="_blank"', popup)

    def test_release_zip_contains_runtime_files_only(self):
        archive_path = ROOT / "dist" / "htmlduckduckgo-chrome.zip"
        self.assertTrue(archive_path.is_file(), "Build the portable release ZIP before running tests.")

        with ZipFile(archive_path) as archive:
            names = set(archive.namelist())
            self.assertEqual(
                names,
                {
                    "manifest.json",
                    "popup.html",
                    "popup.css",
                    "popup.js",
                    "service-worker.js",
                    "assets/icons/icon16.png",
                    "assets/icons/icon48.png",
                    "assets/icons/icon128.png",
                },
            )
            manifest = json.loads(archive.read("manifest.json"))
            self.assertNotIn("chrome_settings_overrides", manifest)
            for name in names:
                if name != "manifest.json":
                    self.assertEqual(archive.read(name), (ROOT / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
