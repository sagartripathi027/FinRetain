import os
import sys
import unittest
import pandas as pd
import tempfile
import shutil

# Ensure current dir is in sys.path
sys.path.append(os.path.dirname(__file__))

from ingestion import load_and_combine_csvs
from validation import validate_dataset

class TestDataLayer(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test CSVs
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)
        
    def create_csv(self, filename, data):
        df = pd.DataFrame(data)
        path = os.path.join(self.test_dir, filename)
        df.to_csv(path, index=False)
        return path

    def test_one_valid_csv(self):
        """Test 1: One valid CSV loads successfully."""
        data = {
            'customer_id': ['C001'],
            'tenure': [10],
            'balance': [100.0],
            'transaction_frequency': [5],
            'complaints': [0],
            'service_usage': [0.8],
            'churn': [0]
        }
        self.create_csv('data1.csv', data)
        df = load_and_combine_csvs(self.test_dir)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['customer_id'], 'C001')

    def test_multiple_valid_csvs(self):
        """Test 2: Multiple valid CSV files can be discovered and combined."""
        data1 = {
            'customer_id': ['C001'],
            'tenure': [10], 'balance': [100.0], 'transaction_frequency': [5],
            'complaints': [0], 'service_usage': [0.8], 'churn': [0]
        }
        data2 = {
            'customer_id': ['C002'],
            'tenure': [20], 'balance': [200.0], 'transaction_frequency': [10],
            'complaints': [1], 'service_usage': [0.9], 'churn': [1]
        }
        self.create_csv('data1.csv', data1)
        self.create_csv('data2.csv', data2)
        df = load_and_combine_csvs(self.test_dir)
        self.assertEqual(len(df), 2)
        self.assertIn('C001', df['customer_id'].values)
        self.assertIn('C002', df['customer_id'].values)

    def test_no_csv_files(self):
        """Test 3: No CSV files produces a clear error."""
        with self.assertRaises(FileNotFoundError):
            load_and_combine_csvs(self.test_dir)

    def test_missing_required_columns(self):
        """Test 4: Missing required columns produces a clear validation error."""
        data = {
            'customer_id': ['C001'],
            'tenure': [10],
            # 'balance' is missing
            'transaction_frequency': [5],
            'complaints': [0],
            'service_usage': [0.8],
            'churn': [0]
        }
        self.create_csv('data_missing.csv', data)
        with self.assertRaises(RuntimeError) as context:
            load_and_combine_csvs(self.test_dir)
        self.assertIn('Missing required columns in dataset', str(context.exception))
        
    def test_invalid_data_values(self):
        """Test for negative values validation."""
        data = {
            'customer_id': ['C001'],
            'tenure': [-5], # Invalid
            'balance': [100.0],
            'transaction_frequency': [5],
            'complaints': [0],
            'service_usage': [0.8],
            'churn': [0]
        }
        self.create_csv('data_invalid.csv', data)
        with self.assertRaises(RuntimeError) as context:
            load_and_combine_csvs(self.test_dir)
        self.assertIn('tenure cannot be negative', str(context.exception))
        
    def test_duplicate_handling(self):
        """Test that duplicate customer records are handled."""
        data1 = {
            'customer_id': ['C001'],
            'tenure': [10], 'balance': [100.0], 'transaction_frequency': [5],
            'complaints': [0], 'service_usage': [0.8], 'churn': [0]
        }
        data2 = {
            'customer_id': ['C001'], # Duplicate ID
            'tenure': [10], 'balance': [100.0], 'transaction_frequency': [5],
            'complaints': [0], 'service_usage': [0.8], 'churn': [0]
        }
        self.create_csv('data1.csv', data1)
        self.create_csv('data2.csv', data2)
        df = load_and_combine_csvs(self.test_dir)
        self.assertEqual(len(df), 1)

if __name__ == '__main__':
    unittest.main()

