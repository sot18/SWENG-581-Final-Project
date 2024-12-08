import unittest
import utils
from unittest.mock import patch
from screenshot_to_code.image_processor import process_image, process_nested_data, recursive_function, convert_to_tailwind_css, convert_to_react_code
from screenshot_to_code.api_handler import get_openai_api_key
from screenshot_to_code.frontend_connector import send_data_to_backend

class TestTruncate(unittest.TestCase):
    
    #Test to test list input
    def test_list(self):
        data = ["this", "is", "a", "test"]
        self.assertEqual(utils.truncate_data_strings(self, data), data)
    
    
    #Test to test a dictionary input
    def test_dictionary(self):
        testDict = {
            1: "this",
            2: "is",
            3: "a",
            4: "test"
        }
        self.assertEqual(utils.truncate_data_strings(self, testDict), testDict)


    #Test to test a dictionary input containing a string over 40 characters
    def test_over_40_chars_dict(self):
        testDict = {"message": "This is a test example string with 46 chars."}
        expectedResults = {"message": "This is a test example string with... (46 chars)"}
        self.assertEqual(utils.truncate_data_strings(self, testDict), expectedResults)
        
    #Test to test a nested dictionary input
    def test_nested_dictionary():
        # Nested dictionary with various string lengths and nested structures
        testData = {
            "level1": {
                "short_string": "short",
                "long_string": "This is a very long string that should be truncated after 40 characters.",
                "nested_dict": {
                    "another_short": "example",
                    "another_long": "Another long string that exceeds forty characters for truncation testing.",
                },
                "nested_list": [
                    "A short string in a list",
                    "A very very very long string in a list that should also be truncated properly.",
                    {
                        "deep_dict_string": "Deeply nested string that is too long to display in its entirety."
                    },
                ],
            }
        }

        # Expected output after truncation
        expectedResults = {
            "level1": {
                "short_string": "short",
                "long_string": "This is a very long string that should... (72 chars)",
                "nested_dict": {
                    "another_short": "example",
                    "another_long": "Another long string that exceeds for... (75 chars)",
                },
                "nested_list": [
                    "A short string in a list",
                    "A very very very long string in a list... (76 chars)",
                    {
                        "deep_dict_string": "Deeply nested string that is too lon... (67 chars)"
                    },
                ],
            }
        }
        
        self.assertEqual(utils.truncate_data_strings(self, testData), expectedResults)
        


      # TC-06: Integration Testing for OpenAI API key
    @patch('screenshot_to_code.api_handler.get_openai_api_key', return_value='test_api_key')
    def test_openai_api_key_handling(self, mock_key):
        key = get_openai_api_key()
        self.assertEqual(key, 'test_api_key')

    # TC-07: Integration Testing for frontend-to-backend communication
    @patch('screenshot_to_code.frontend_connector.send_data_to_backend', return_value={'status_code': 200, 'message': 'Success'})
    def test_frontend_to_backend_communication(self, mock_send):
        input_data = {'input': 'test'}
        response = send_data_to_backend(input_data)
        self.assertEqual(response['status_code'], 200)
        self.assertEqual(response['message'], 'Success')
  


if __name__ == '__main__':
    unittest.main()

