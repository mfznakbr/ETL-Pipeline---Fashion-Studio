import pytest
import pandas as pd
import sys
import os
# Tambahkan parent directory ke Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.transform import (  # Ganti 'transform' dengan nama file modul Anda
    transform_to_dataframe,
    is_row_dirty,
    clean_and_transform,
    transform_price,
    remove_duplicates_and_nulls
)

# Sample data untuk testing
SAMPLE_DATA = [
    {
        "Title": "Product A",
        "Rating": "Rating: ⭐ 4.5 / 5",
        "Price": "$100",
        "Size": "Size: M",
        "Gender": "Gender: Male",
        "Colors": "Colors: Red"
    },
    {
        "Title": "Unknown Product",
        "Rating": "Invalid Rating / 5",
        "Price": "Price Unavailable",
        "Size": "Size: L",
        "Gender": "Gender: Female",
        "Colors": "Colors: Blue"
    },
    {
        "Title": "Product B",
        "Rating": "3 / 5",
        "Price": "$200",
        "Size": "Size: XL",
        "Gender": "Gender: Unisex",
        "Colors": "Colors: Green"
    }
]


DIRTY_PATTERNS = {
    "Title": ["Unknown Product"],
    "Rating": ["Invalid Rating / 5"],
    "Price": ["Price Unavailable"]
}

def test_transform():
    df = transform_to_dataframe(SAMPLE_DATA)
    print("Data telah dikonversi ke dataframe :")
    print(df)
    
    df = is_row_dirty(df, DIRTY_PATTERNS)
    print("Data setelah menjalankan fungsi is_row_dirty : ")
    print(df)
    
    df = df.apply(clean_and_transform, axis=1)
    print("Data setelah dibersihkan dan di transform : ")
    print(df)
    
    df = transform_price(df, exchange_rate=16000)
    print("Data setelah harga di konversi dari Us dolar ke rupiah : ")
    print(df)
    
    df = remove_duplicates_and_nulls(df)
    print("Data telah dihapus nilai duplicate dan nulls : ")
    print(df)
    
    
    assert not df.empty
    assert 'invalid' not in df['Rating'].values


if __name__ == "__main__":
    print("\n=== MEMULAI TEST ===")
    try:
        test_transform()
    except AssertionError as e:
        print("\n❌ Test gagal:", str(e))
    except Exception as e:
        print("\n⚠️ Terjadi error:", str(e))
    finally:
        print("\n=== TEST SELESAI ===")