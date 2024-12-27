import unittest
from unittest.mock import patch, MagicMock
from database.database import insert_job  # Adjust the import according to your structure

class TestDatabase(unittest.TestCase):
    
    @patch('sqlite3.connect')  # This mocks sqlite3.connect
    def test_insert_job(self, mock_connect):
        # Create a mock database connection and cursor
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value = mock_cursor  # Return the mock cursor when cursor() is called
        
        # Mock the connect_db call to return the mock database connection
        mock_connect.return_value = mock_db
        
        # Define a sample job
        job = {
            'uniqueId': 'job-123',
            'jobTitle': 'Software Developer',
            'jobCompany': 'Company XYZ',
            'jobLocation': 'New York',
            'jobSalary': '$100,000',
            'jobCategory': 'Engineering',
            'jobSubCategory': 'Development',
            'jobListingDate': '2024-01-01',
            'jobURL': 'http://example.com/job-123'
        }
        
        # Call the function to test
        insert_job(job)
        
        # Print the arguments that were passed to execute (for debugging)
        # print("Call args for execute:", mock_cursor.execute.call_args_list)
        
        # Clean up the actual and expected query by removing unnecessary whitespace
        expected_query = '''
            INSERT INTO jobs (
                uniqueId, jobTitle, jobCompany, jobLocation, 
                jobSalary, jobCategory, jobSubCategory, 
                jobListingDate, jobURL
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''.strip()

        # Normalize both the expected and actual queries to remove extra spaces and line breaks
        def normalize_query(query):
            return " ".join(query.strip().split())

        # Normalize actual and expected queries
        actual_query = normalize_query(mock_cursor.execute.call_args_list[0][0][0])
        normalized_expected_query = normalize_query(expected_query)
        #print(actual_query)

        # Verify that the execute method was called with the correct SQL and parameters
        self.assertEqual(actual_query, normalized_expected_query)  # Compare SQL queries
        
        # Verify parameters
        expected_params = (
            job['uniqueId'],
            job['jobTitle'],
            job['jobCompany'],
            job['jobLocation'],
            job['jobSalary'],
            job['jobCategory'],
            job['jobSubCategory'],
            job['jobListingDate'],
            job['jobURL']
        )
        actual_params = mock_cursor.execute.call_args_list[0][0][1]
        self.assertEqual(actual_params, expected_params)  # Compare parameters

if __name__ == '__main__':
    unittest.main()
