# tests/test_scraper.py
import unittest
from scraper.scraper import fetch_data
from unittest.mock import patch

class TestScraper(unittest.TestCase):

    @patch('scraper.scraper.requests.get')  # Mocking requests.get to avoid actual HTTP requests
    def test_fetch_data(self, mock_get):
        # Load real HTML content from the saved file
        with open('tests/mock_jobstreet.html', 'r', encoding='utf-8') as file:
            real_html_content = file.read()

        # Define what the mock should return
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        # Simulating a more realistic HTML structure with job listings
        mock_response.text = real_html_content
            
        #print(mock_response.text)

        # Call the function to test
        url = "http://example.com/jobs"
        result = fetch_data(url)
        #print(result[0])

        # Check that fetch_data returns the expected result
        self.assertIsInstance(result, list)  # It should return a list
        self.assertGreater(len(result), 0)  # It should contain at least one job listing
        self.assertIn('jobTitle', result[0])  # Job title should be in the first item
        #self.assertEqual(result[0]['jobTitle'], 'Software Developer')  # First job title should match
        #self.assertEqual(result[1]['jobTitle'], 'Data Scientist')  # Second job title should match
        self.assertIn('jobCompany', result[0])  # Job company should be in the first item

if __name__ == '__main__':
    unittest.main()
