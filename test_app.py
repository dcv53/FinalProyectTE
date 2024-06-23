import unittest
import pandas as pd
import sqlite3

class TestApp(unittest.TestCase):

    def test_data_integrity(self):
        df = pd.read_json('data.json', lines=True)
        self.assertFalse(df.empty)
        self.assertIn('Region', df.columns)
        self.assertIn('Country', df.columns)
        self.assertIn('Language', df.columns)
        self.assertIn('Time', df.columns)
        
    def test_sqlite_data(self):
        conn = sqlite3.connect('countries.db')
        df_sql = pd.read_sql('SELECT * FROM countries', conn)
        conn.close()
        
        df_json = pd.read_json('data.json', lines=True)
        
        self.assertTrue(df_sql.equals(df_json))
    
    def test_time_statistics(self):
        df = pd.read_json('data.json', lines=True)
        
        total_time = df['Time'].sum()
        average_time = df['Time'].mean()
        min_time = df['Time'].min()
        max_time = df['Time'].max()
        
        self.assertGreater(total_time, 0)
        self.assertGreaterEqual(average_time, 0)
        self.assertGreaterEqual(min_time, 0)
        self.assertGreaterEqual(max_time, 0)

if __name__ == '__main__':
    unittest.main()