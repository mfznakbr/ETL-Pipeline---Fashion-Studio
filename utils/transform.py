import pandas as pd
import re


def transform_to_dataframe(data):
    "Ubah data jadi dataframe"
    if not isinstance(data, list):
        raise ValueError("data harus berupa list atau dict")
    if len(data) == 0: 
        raise ValueError ("Data kosong")
    df = pd.DataFrame(data)
    return df

def is_row_dirty(data, dirty_patterns):
    "Buang baris yang mengandung pola 'kotor'"
    if not isinstance(dirty_patterns, dict):
        raise ValueError("dirty paterrns harus berupa dictionary")
    
    for column, patterns in dirty_patterns.items():
        if column in data.columns:
            data = data[~data[column].isin(patterns)]
    return data


def clean_and_transform(data):
    # hapus karakter yang tidak digunakan
    # pembershihan kolom rating
    data['Rating'] = re.sub(r'Rating: ⭐\s*', '', str(data['Rating']))
    data['Rating'] = re.sub(r'\s*/\s*5', '', data['Rating'])
    data['Rating'] = data['Rating'].strip()
    
    # pembersihan kolom size
    data['Size'] = re.sub(r'Size:\s*', '', data['Size'])
    data['Size'] = data['Size'].strip()
    
    # Pembersihan kolom Gender
    data['Gender'] = re.sub(r'Gender:\s*', '', data['Gender'])
    data['Gender'] = data['Gender'].strip()
    
    #Pembersihan kolom Colors
    data['Colors'] = re.sub(r'\s*Colors$', '', str(data['Colors']))
    data['Colors'] = data['Colors'].strip()
    
    try:
        data['Rating'] = float(data['Rating'])
        data['Colors'] = int(data['Colors'])
    except:
        pass
    
    return data


def transform_price(data, exchange_rate):
    try:
        data['Price_in_dolar'] = data['Price'].replace({r'\$': '', r',':''}, regex=True).astype(float)
    
        data['Price'] = (data['Price_in_dolar'] * exchange_rate).round(2)
    
        data = data.drop(columns=['Price_in_dolar'])
    except Exception as e:
        print(f"error saat mengubah harga : {e}")
    
    return data


def remove_duplicates_and_nulls(data):
    """Remove duplicate rows and null values."""
    try:
        return data.drop_duplicates().dropna()
    except Exception as e:
        print(f"error saat membersihkan duplikat atau null : {e}")
    return data
    
    