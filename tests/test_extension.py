import json
import unittest
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent


class ExtensionPackageTests(unittest.TestCase):
    def test_manifest_configures_default_html_search_and_popup(self):
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

        self.assertEqual(manifest["manifest_version"], 3)
        provider = manifest["chrome_settings_overrides"]["search_provider"]
        self.assertTrue(provider["is_default"])
        self.assertEqual(
            provider["search_url"],
            "https://html.duckduckgo.com/html/?q={searchTerms}",
        )
        self.assertEqual(manifest["action"]["default_popup"], "popup.html")
        self.assertNotIn("permissions", manifest)
        self.assertNotIn("host_permissions", manifest)

    def test_popup_submits_searches_to_html_endpoint(self):
        popup = (ROOT / "popup.html").read_text(encoding="utf-8")

        self.assertIn('action="https://html.duckduckgo.com/html/"', popup)
        self.assertIn('method="get"', popup)
        self.assertIn('name="q"', popup)
        self.assertIn('target="_blank"', popup)

    def test_release_zip_contains_runtime_files_only(self):
        archive_path = ROOT / "dist" / "htmlduckduckgo-chrome.zip"
        self.assertTrue(archive_path.is_file(), "Build the release ZIP before running tests.")

        with ZipFile(archive_path) as archive:
            names = set(archive.namelist())
            self.assertEqual(
                names,
                {
                    "manifest.json",
                    "popup.html",
                    "popup.css",
                    "popup.js",
                    "assets/icons/icon16.png",
                    "assets/icons/icon48.png",
                    "assets/icons/icon128.png",
                },
            )
            for name in names:
                self.assertEqual(archive.read(name), (ROOT / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
