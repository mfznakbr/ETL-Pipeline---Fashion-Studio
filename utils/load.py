from sqlalchemy import create_engine
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import logging

# Setup logging untuk debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_csv(data, nama_file):
    return data.to_csv(nama_file, index=False)


Base_dir = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT = os.path.join(Base_dir, 'google_sheet_API.json')
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']


credential = Credentials.from_service_account_file(SERVICE_ACCOUNT, scopes=SCOPE)
def save_to_gsheet(data, range_name, spreadsheet_id):
    try:
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()
    
    # persiapan data untuk dikirim
        values = [data.columns.tolist()] + data.values.tolist()
        body = {'values':values}
    
    # kirim data ke googlesheets
        result = sheet.values().update(
            spreadsheetId= spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body = body
        ).execute()
    
        print("Data scraping berhasil dikirim ke google sheets")
        return result 
    except HttpError as eror:
        print(f"Terjadi kesalahan HTTP error saat mengirim data ke google sheets: {eror}")
    except Exception as e:
        print(f"Terjadi error tidak terduga : {e}")
        
def store_to_postgre(data, db_url):
    """Fungsi untuk menyimpan data ke dalam PostgreSQL."""
    try:
        # Membuat engine database
        engine = create_engine(db_url)
        
        # Menyimpan data ke tabel 'bookstoscrape' jika tabel sudah ada, data akan ditambahkan (append)
        with engine.connect() as con:
            data.to_sql('fashionproductscrape', con=con, if_exists='append', index=False)
            print("Data berhasil ditambahkan ke database!")
            return True
    
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data: {e}")
        return False