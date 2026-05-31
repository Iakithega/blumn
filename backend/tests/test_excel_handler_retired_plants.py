import unittest

from openpyxl import Workbook

from backend.app.core.excel_handler import ExcelHandler, is_retired_plant


class RetiredPlantRegistryTest(unittest.TestCase):
    def test_marks_hoya_mathilde_as_retired(self):
        self.assertTrue(is_retired_plant("Hoya Mathilde"))

    def test_keeps_hoya_sabah_current(self):
        self.assertFalse(is_retired_plant("Hoya Sabah"))

    def test_normalizes_case_and_extra_spaces(self):
        self.assertTrue(is_retired_plant("  hoya   mathilde  "))


class ActivePlantListTest(unittest.TestCase):
    def test_get_plant_names_skips_retired_plants(self):
        wb = Workbook()
        ws = wb.active
        ws.append(["date", "plant name"])
        ws.append(["20.05.2026", "Hoya Mathilde"])
        ws.append(["20.05.2026", "Hoya Sabah"])

        handler = ExcelHandler.__new__(ExcelHandler)
        plant_names = handler._get_plant_names(ws)

        self.assertEqual(plant_names, ["Hoya Sabah"])


if __name__ == "__main__":
    unittest.main()
