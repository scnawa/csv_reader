import unittest
from unittest.mock import patch
import pandas as pd
import yaml
from main import readCsv, formatYaml, selectTopRecords
from io import StringIO

# Assuming your functions are in a file called script.py
# from script import readCsv, selectTopRecords, formatYaml

class TestCSVProcessing(unittest.TestCase):
    
    # Test readCsv function: Test CSV data reading and type conversion
    @patch('pandas.read_csv')
    def test_readCsv(self, mock_read_csv):
        # Mock CSV data
        mock_data = {
            'firstname': ['John', 'Jane', 'Alice'],
            'lastname': ['Doe', 'Smith', 'Brown'],
            'division': ['2', '1', '3'],  # Initially as strings
            'points': ['10', '20', '30'],  # Initially as strings
            'date': ['2024-11-09', '2024-11-10', '2024-11-11'],
            'summary': ['Task A', 'Task B', 'Task C']
        }
        mock_df = pd.DataFrame(mock_data)
        mock_read_csv.return_value = mock_df
        
        # Read CSV file (we don't care about the actual file in the test)
        file_path = 'dummy.csv'
        df = readCsv(file_path)
        
        # Check if 'division' and 'points' were correctly converted to integers
        self.assertEqual(df['division'].dtype, 'int64')
        self.assertEqual(df['points'].dtype, 'int64')
        self.assertEqual(len(df), 3)  # There should be 3 records in the mock data
    
    # Test selectTopRecords function: Test sorting and selecting top records
    def test_selectTopRecords(self):
        # Sample DataFrame
        data = {
            'firstname': ['John', 'Jane', 'Alice'],
            'lastname': ['Doe', 'Smith', 'Brown'],
            'division': [2, 1, 3],
            'points': [10, 20, 30],
            'date': ['2024-11-09', '2024-11-10', '2024-11-11'],
            'summary': ['Task A', 'Task B', 'Task C']
        }
        df = pd.DataFrame(data)

        # Get top 3 sorted by 'points'
        top_records = selectTopRecords(df)

        # Verify top records are sorted by 'points' in descending order
        self.assertEqual(len(top_records), 3)
        self.assertEqual(top_records.iloc[0]['points'], 30)  # Highest points should come first
        self.assertEqual(top_records.iloc[1]['points'], 20)
        self.assertEqual(top_records.iloc[2]['points'], 10)
    
    # Test formatYaml function: Test YAML formatting
    def test_formatYaml(self):
        # Sample DataFrame
        data = {
            'firstname': ['John', 'Jane', 'Alice'],
            'lastname': ['Doe', 'Smith', 'Brown'],
            'division': [2, 1, 3],
            'points': [10, 20, 30],
            'date': ['2024-11-09', '2024-11-10', '2024-11-11'],
            'summary': ['Task A', 'Task B', 'Task C']
        }
        df = pd.DataFrame(data)

        # Get top 3 sorted by 'points'
        top_records = selectTopRecords(df)

        # Get the YAML output
        yaml_output = formatYaml(top_records)

        # Check if the YAML output is as expected
        expected_yaml = """records:
- name: John Doe
  details: In division 2 from 2024-11-09 performing Task A
- name: Jane Smith
  details: In division 1 from 2024-11-10 performing Task B
- name: Alice Brown
  details: In division 3 from 2024-11-11 performing Task C
"""
        # Compare the generated YAML to the expected YAML
        self.assertEqual(yaml_output.strip(), expected_yaml.strip())
    
    # Test for File Not Found (edge case handling)
    @patch('builtins.print')
    @patch('sys.exit')
    def test_file_not_found(self, mock_exit, mock_print):
        file_path = 'non_existent_file.csv'
        
        # Simulate FileNotFoundError
        with self.assertRaises(SystemExit):
            readCsv(file_path)
        
        mock_print.assert_called_with(f"File '{file_path}' not found.")
        mock_exit.assert_called_with(1)

if __name__ == "__main__":
    unittest.main()