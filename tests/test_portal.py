import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_URL = "https://mahayytest4.github.io/ayyashking-themes"
SUPPORT_EMAIL = "mahmoud.ayyash09@gmail.com"


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.links.append(values[attribute])


class PublisherPortalContractTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_required_public_pages_and_assets_exist(self):
        expected = {
            "index.html",
            "404.html",
            "assets/styles.css",
            "assets/app.js",
            "themes/stratfold/index.html",
            "support/index.html",
            "support/thanks.html",
            "privacy/index.html",
        }
        missing = sorted(path for path in expected if not (ROOT / path).is_file())
        self.assertEqual([], missing)

    def test_portal_links_to_stratfold_documentation_and_support(self):
        page = self.read("index.html")
        self.assertIn('href="themes/stratfold/"', page)
        self.assertIn('href="support/"', page)
        self.assertIn("AyyashKing", page)
        self.assertIn("Sunday–Thursday", page)
        self.assertIn("10:00–18:00", page)
        self.assertNotIn("example.com", page)

    def test_stratfold_documentation_covers_real_theme_workflows(self):
        page = self.read("themes/stratfold/index.html")
        for required in (
            "Stratfold",
            "Version 0.1.0",
            "Install the theme",
            "Material index",
            "Specimen ledger",
            "Sample pathway",
            "Selling plans",
            "Pickup availability",
            "English and Arabic",
            "Theme Editor",
            "Contact support",
        ):
            self.assertIn(required, page)
        self.assertIn('../../support/', page)
        self.assertNotIn("Lorem ipsum", page)
        self.assertNotIn("example.com", page)

    def test_support_form_meets_shopify_contact_requirements(self):
        page = self.read("support/index.html")
        self.assertRegex(
            page,
            re.compile(
                rf'<form[^>]+action="https://formsubmit\.co/{re.escape(SUPPORT_EMAIL)}"[^>]+method="POST"[^>]+enctype="multipart/form-data"',
                re.IGNORECASE,
            ),
        )
        for field_name in (
            "first_name",
            "last_name",
            "email",
            "store_url",
            "description",
            "attachment",
            "theme_name",
            "_subject",
            "_autoresponse",
            "_next",
        ):
            self.assertIn(f'name="{field_name}"', page)
        self.assertIn('value="Stratfold"', page)
        self.assertIn(f'value="{PUBLIC_URL}/support/thanks.html"', page)
        self.assertIn('accept="image/png,image/jpeg,image/webp,application/pdf"', page)
        self.assertNotIn('name="_captcha" value="false"', page)
        self.assertRegex(page, re.compile(r'<input[^>]+type="file"[^>]+data-max-bytes="10485760"', re.I))
        self.assertIn('class="form-error"', page)
        self.assertNotRegex(
            page,
            re.compile(r'name="(?:password|access[_ -]?token|api[_ -]?key)"', re.I),
        )

    def test_pages_have_accessibility_and_bilingual_hooks(self):
        for path in (
            "index.html",
            "themes/stratfold/index.html",
            "support/index.html",
            "support/thanks.html",
            "privacy/index.html",
        ):
            page = self.read(path)
            self.assertIn('<html lang="en"', page, path)
            self.assertIn('class="skip-link"', page, path)
            self.assertIn('id="main-content"', page, path)
            self.assertIn('data-language-toggle', page, path)
            self.assertIn('data-i18n="skip-link"', page, path)
            self.assertIn('data-i18n="nav-support"', page, path)
            self.assertIn('data-title-en=', page, path)
            self.assertIn('data-title-ar=', page, path)
            self.assertIn('class="no-script-language"', page, path)
            self.assertIn('[data-lang-panel][hidden]', page, path)
            self.assertIn('lang="ar" dir="rtl"', page, path)

    def test_stratfold_docs_include_metafields_faq_and_critical_support(self):
        page = self.read("themes/stratfold/index.html")
        for required in (
            "specimen.finish",
            "specimen.scale",
            "specimen.applications",
            "specimen.evidence",
            "specimen.sample_product",
            "specimen.parent_product",
            "specimen.is_sample",
            "Frequently asked questions",
            "الأسئلة الشائعة",
            "Critical theme bugs",
            "الأعطال الحرجة",
        ):
            self.assertIn(required, page)

    def test_privacy_discloses_hosting_storage_and_retention(self):
        page = self.read("privacy/index.html")
        for required in (
            "GitHub Pages",
            "IP address",
            "localStorage",
            "ayyashking-language",
            "12 months",
            "عنوان IP",
        ):
            self.assertIn(required, page)

    def test_all_local_links_and_assets_resolve(self):
        missing = []
        for html_path in ROOT.rglob("*.html"):
            collector = LinkCollector()
            collector.feed(html_path.read_text(encoding="utf-8"))
            for raw_link in collector.links:
                if raw_link.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                clean = urlsplit(raw_link).path
                if not clean:
                    continue
                if clean.startswith("/ayyashking-themes/"):
                    target = ROOT / clean.removeprefix("/ayyashking-themes/")
                else:
                    target = html_path.parent / clean
                if clean.endswith("/"):
                    target = target / "index.html"
                if not target.resolve().is_file():
                    missing.append(f"{html_path.relative_to(ROOT)} -> {raw_link}")
        self.assertEqual([], sorted(missing))

    def test_mobile_overflow_guards_cover_docs_and_no_js_forms(self):
        styles = self.read("assets/styles.css")
        self.assertRegex(styles, re.compile(r"\.docs-content\s*\{[^}]*min-width:\s*0", re.S))
        self.assertRegex(styles, re.compile(r"\.table-wrap\s*\{[^}]*overflow-x:\s*auto", re.S))
        self.assertRegex(styles, re.compile(r"\.docs-content\s+h1\s*\{[^}]*overflow-wrap:\s*anywhere", re.S))
        self.assertRegex(styles, re.compile(r"\.code-line,\s*code\s*\{[^}]*overflow-wrap:\s*anywhere", re.S))
        honey = re.search(r"\.honey\s*\{([^}]*)\}", styles, re.S)
        self.assertIsNotNone(honey)
        self.assertNotRegex(honey.group(1), re.compile(r"-\d{4,}px"))
        self.assertRegex(honey.group(1), re.compile(r"clip(?:-path)?:"))

    def test_static_assets_avoid_tracking_and_remote_scripts(self):
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix not in {".html", ".css", ".js"}:
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, re.compile(r"google-analytics|googletagmanager|facebook\.net", re.I), str(path))
            if path.suffix == ".html":
                self.assertNotRegex(text, re.compile(r'<script[^>]+src=["\']https?://', re.I), str(path))


if __name__ == "__main__":
    unittest.main()
