import os
import sys
import unittest
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import thai_ocr


class TestThaiCleaning(unittest.TestCase):
    def test_sara_am_preservation(self):
        """Ensure common words with spaces before Sara Aa are NOT wrongly turned into Sara Am."""
        # 'ม า' should NEVER become 'นำ'
        cleaned = thai_ocr.clean_thai_text("ม า")
        self.assertNotIn("นำ", cleaned)
        self.assertIn("า", cleaned)

        # 'ต า' should NEVER become 'ตำ'
        cleaned = thai_ocr.clean_thai_text("ต า")
        self.assertNotIn("ตำ", cleaned)
        self.assertIn("า", cleaned)

        # 'ห า' should NEVER become 'หำ'
        cleaned = thai_ocr.clean_thai_text("ห า")
        self.assertNotIn("หำ", cleaned)
        self.assertIn("า", cleaned)

        # 'ย า' should NEVER become 'ยำ'
        cleaned = thai_ocr.clean_thai_text("ย า")
        self.assertNotIn("ยำ", cleaned)
        self.assertIn("า", cleaned)

    def test_decomposed_sara_am_recovery(self):
        """Ensure decomposed Sara Am with tone mark is properly recovered."""
        # น้ า -> น้ำ
        cleaned = thai_ocr.clean_thai_text("น้ า")
        self.assertEqual(cleaned, "น้ำ")

        # ซ ้า -> ซ้ำ
        cleaned = thai_ocr.clean_thai_text("ซ ้า")
        self.assertEqual(cleaned, "ซ้ำ")

        # Nikhahit + Sara Aa (e.g. จํากัด -> จำกัด)
        cleaned = thai_ocr.clean_thai_text("จ\u0E4D\u0E32กัด")
        self.assertEqual(cleaned, "จำกัด")

    def test_pua_recovery(self):
        """Ensure shifted PUA characters are normalized to standard Thai Unicode."""
        # 0xF711 is shifted สระอี (0x0E35), 0xF70A is shifted ไม้เอก (0x0E48)
        pua_text = "ท\uF711\uF70A"  # ท + สระอี shifted + ไม้เอก shifted
        cleaned = thai_ocr.clean_thai_text(pua_text)
        self.assertEqual(cleaned, "ที่")

    def test_zero_width_space_removal(self):
        """Ensure zero-width spaces are stripped."""
        text_with_zwsp = "ภาษา\u200bไทย\ufeff"
        cleaned = thai_ocr.clean_thai_text(text_with_zwsp)
        self.assertEqual(cleaned, "ภาษาไทย")

    def test_heading_heuristic(self):
        """Ensure numeric statistics are not mistakenly converted to Markdown headings."""
        class MockPage:
            def get_text(self, mode):
                return [
                    (0, 0, 100, 20, "หมวดที่ 1 บททั่วไป\n"),
                    (0, 30, 100, 50, "1. บทนำ\n"),
                    (0, 60, 100, 80, "50 % ของประชากรเห็นด้วย\n"),
                    (0, 90, 100, 110, "100 บาท ต่อคน\n"),
                ]

        mock_page = MockPage()
        result = thai_ocr.extract_page_text_blocks(mock_page)

        # Headings should have ### prefix
        self.assertIn("### หมวดที่ 1 บททั่วไป", result)
        self.assertIn("### 1. บทนำ", result)

        # Non-headings should NOT have ### prefix
        self.assertNotIn("### 50 %", result)
        self.assertNotIn("### 100 บาท", result)
        self.assertIn("50 % ของประชากรเห็นด้วย", result)
        self.assertIn("100 บาท ต่อคน", result)


if __name__ == "__main__":
    unittest.main()
