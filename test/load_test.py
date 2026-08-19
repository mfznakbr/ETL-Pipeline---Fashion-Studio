import pandas as pd
import sys
import os
import pytest
# Tambahkan parent directory ke Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.load import save_csv, save_to_gsheet, store_to_postgre

def test_load():
    # data dummy 5 baris x 5 kolom
    data_dummy = pd.DataFrame(
        {
            'Nama' : ['Fauzan', 'Kalvin', 'Judith', 'Ditha', 'Ita'], 
            'Nim': [2205171008, 2205171010, 2205171011, 2205171031, 2205171007],
            'Umur' : [20, 21, 22, 21, 21],
            'IPK' : [4.0, 3.5, 3.9, 3.7, 3.8],
            'Program studi' : ['Manajemen Bisnis', 'Manajemen Bisnis', 'Manajemen Bisnis', 'Manajemen Bisnis', 'Manajemen Bisnis']
        }
    )
    # 1. Simpan ke CSV 
    save_csv(data_dummy, 'data_dummy.csv')
    
    # 2. Simpan ke google sheets
    SPREADSHEET_ID = '144FijbSlj5Cd_-oChq2I6o3yo9Y1hxIwGBb22U5mF5E'
    RANGE_NAME = 'Sheet1!A1'
    save_to_gsheet(data_dummy, RANGE_NAME, SPREADSHEET_ID)
    
    # 3. simpan ke database postgres
    db_url = 'postgresql+psycopg2://mhd_fauzan:fznakbr@localhost:5432/test_load'
    store_to_postgre(data_dummy, db_url)
    
if __name__ == '__main__':
    test_load()