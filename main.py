import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.extract import scrape_product_fashion
from utils.transform import (  
    transform_to_dataframe,
    is_row_dirty,
    clean_and_transform,
    transform_price,
    remove_duplicates_and_nulls
)
from utils.load import save_csv, store_to_postgre, save_to_gsheet

def main():
    """Fungsi utama untuk keseluruhan proses ETL (EXTRACT, TRANSFORM, LOAD)"""
    
    BASE_URL = 'https://fashion-studio.dicoding.dev'
    try:
        
        """
            MENJALANKAN TAHAPAN EXTRACT (extract.py)       
        """
        fashion_data = scrape_product_fashion(BASE_URL)
        if not fashion_data:
             print("X tidak ada data yang berhasil diambil")
             return
         
        """
            TAHAPAN TRANSFORM (transform.py)
        """
        
        dirty_patterns = {
            "Title": ["Unknown Product", "Tidak Ada"],
            "Rating": ["Invalid Rating", "Rating: Not Rated", "Tidak Ada"],
            "Price": ['Tidak Ada']
        }

        df = transform_to_dataframe(fashion_data)
        df = is_row_dirty(df, dirty_patterns)
        df = df.apply(clean_and_transform, axis=1)
        df = transform_price(df, exchange_rate=16000)
        df = remove_duplicates_and_nulls(df)

        
        print(df.head(10))
        print(df.info())
        
        """
            TAHAPAN AKHIR LOAD (load.py)
        """
        
        print(save_csv(df, nama_file='product_fashion0.csv'))
        
        SPREADSHEET_ID = '1B_h4EXRdFhhfQmJfSqu2vr--5Apm2IXrsjys8QUGILU'
        RANGE_NAME = 'Sheet1!A1'
        save_to_gsheet(df, RANGE_NAME, SPREADSHEET_ID)
        
        db_url = 'postgresql+psycopg2://mhd_fauzan:fznakbr@localhost:5432/fashionproduct_db'
        store_to_postgre(df, db_url)
    except Exception as e:
        print(f"\n❌ Error utama: {str(e)}")
        
 
if __name__ == '__main__':
    main()