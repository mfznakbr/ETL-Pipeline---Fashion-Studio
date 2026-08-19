import pytest
from unittest.mock import patch
import sys
import os
# Tambahkan parent directory ke Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.extract import (  # Pastikan untuk mengganti 'extract' sesuai nama modul
    fetching_content,
    extract_data_produk_fashion,
    scrape_product_fashion
)

# Uji untuk ambil konten html dari url
def test_fetching():
    url = "https://fashion-studio.dicoding.dev"
    with patch('requests.Session.get') as get_mock:
        get_mock.return_value.status_code = 200
        get_mock.return_value.content = b"Mock kontent"
        
        content = fetching_content(url)
        assert content == b"Mock kontent", "Konten tidak dapat diambil"
        
# Uji untuk ekstraksi data produk fashion
def test_extract_datafashion():
    from bs4 import BeautifulSoup
    
    html =  """
    <div class="product-details">
        <h3 class="product-title">Produk Fashion Contoh</h3>
        <div class="price-container">
            <span class="price">$50</span>
        </div>
        <p style="font-size: 14px; color: #777;">4.5/5</p>
        <p style="font-size: 14px; color: #777;">Red, Blue</p>
        <p style="font-size: 14px; color: #777;">L, XL</p>
        <p style="font-size: 14px; color: #777;">Unisex</p>
    </div>
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    produk = soup.find('div', class_='product-details')
    
    data = extract_data_produk_fashion(produk)
    
    assert data['Title'] == 'Produk Fashion Contoh'
    assert data['Price'] == '$50'
    assert data['Rating'] == '4.5/5'
    assert data['Colors'] == 'Red, Blue'
    assert data['Size'] == 'L, XL'
    assert data['Gender'] == 'Unisex'

def test_scrape_product():
    mock_html = """
    <html>
        <div class="product-details">
            <h3 class="product-title">Mock Hoodie Naruto</h3>
            <div class="price-container"><span class="price">$45</span></div>
            <p style="font-size: 14px; color: #777;">4.8 / 5</p>
            <p style="font-size: 14px; color: #777;">2 Colors</p>
            <p style="font-size: 14px; color: #777;">Size : M</p>
            <p style="font-size: 14px; color: #777;">Gender : Man</p>
        </div>
    </html>
    """
    
    with patch('requests.Session.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = mock_html.encode()
        
        base_url = "https://fashion-studio.dicoding.dev"
        data = scrape_product_fashion(base_url, delay=0) 
        
        assert len(data) == 1
        assert data[0]['Title'] == 'Mock Hoodie Naruto'
        assert data[0]['Price'] == '$45'
        assert data[0]['Rating'] == '4.8 / 5'
        assert data[0]['Colors'] == '2 Colors'
        assert data[0]['Size'] == 'Size : M'
        assert data[0]['Gender'] == 'Gender : Man'
        
# Menjalankan semua test 
def run_test():
    test_fetching()
    test_extract_datafashion()
    test_scrape_product()
    print("Semua test berhasil dijalankan")
    
if __name__ == "__main__":
    run_test()