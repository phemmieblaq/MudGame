import unittest
import HtmlTestRunner

from script.character import validate_height, validate_gender, validate_race


class TestCharacterCreation(unittest.TestCase):
    def test_validate_height_valid_input(self):
        valid_height = "180"
        result = validate_height(valid_height)
        self.assertEqual(result, 180.0)
    #

    def test_validate_gender_valid_input(self):
        valid_gender = "Male"
        result = validate_gender(valid_gender)
        self.assertEqual(result, "male")


    def test_validate_race_valid_input(self):
        valid_race = "Human"
        result = validate_race(valid_race)
        self.assertEqual(result, "Human")


    # def test_invalidate_race_valid_input(self):
    #     valid_race = ""
    #     result = validate_race(valid_race)
    #     self.assertEqual(result, "")






if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test_reports'))
