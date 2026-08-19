import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime


HEADERS = {
    "User-Agent" : (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    """
    MENGAMBIL KONTEN HTML DARI URL YANG DI BERIKAN
    """
    sesi = requests.Session()
    response = sesi.get(url, headers=HEADERS)
    
    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as exp:
        print(f"Terjadi kesalahan ketika melakukan requests")
        return None
    
def extract_data_produk_fashion(produk_details):
    """
    MENGAMBIL DATA DENGAN EROR HANDLING
    """
    data_default = {
        "Title" : "Tidak Ada",
        "Price" : "Tidak Ada",
        "Rating" : "Tidak Ada",
        "Colors" : "Tidak Ada",
        "Size" : "Tidak Ada",
        "Gender" : "Tidak Ada"
    }
    
    try:
        # ekstrak untuk judul 
        title_product = produk_details.find('h3', class_='product-title')
        title = title_product.text.strip() if title_product else data_default["Title"]
        
        # Ekstrak untuk harga
        price = data_default["Price"]
        price_container = produk_details.find('div', class_='price-container')
        if price_container:
            price_elem = price_container.find('span', class_='price')
            if price_elem:
                price = price_elem.text.strip()
                
        # Ekstrak atribut rating, color, size, dan gender
        p_elem = produk_details.find_all('p', style="font-size: 14px; color: #777;")
        atribut ={  
            "Rating": data_default["Rating"],
            "Colors": data_default["Colors"],
            "Size" : data_default["Size"],
            "Gender": data_default["Gender"]
        }
        
        for detail, key in enumerate(["Rating", "Colors", "Size", "Gender"]):
            if detail < len(p_elem):
                atribut[key] = p_elem[detail].text.strip()
                
        return {
            "Title" : title,
            "Price" : price,
            **atribut,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        print(f"Error saat proses ekstraksi : {e}")
        return data_default
    
    
def scrape_product_fashion(base_url, start_page=1, delay=2):
    max_pages = 50
    data = []
    uniq_title = set()
    
    for page in range(start_page, max_pages + 1):
        url = f"{base_url.rstrip('/')}/page{page}" if page > 1 else base_url
        print(f"\n Halaman {page} : {url}")
        
        content = fetching_content(url)
        if not content:
            print("Gagal mendapatkan konten")
            break
        soup = BeautifulSoup(content, "html.parser")
        product_fashion = soup.find_all('div', class_='product-details')
        
        if not product_fashion:
            print("Tidak ada produk")
            break
        
        print(f"produk yang ditemukan adalah {len(product_fashion)} produk")
        
        for i, product in enumerate(product_fashion, 1):
            product_data = extract_data_produk_fashion(product)
            print(f"{i}. {product_data["Title"]} == {product_data['Price']}")
            data.append(product_data)  


                
        next_btn = soup.find('li', class_='page-item next')
        if not next_btn or 'disabled' in next_btn.get('class', []):
            print("⏹️ Tidak ada halaman berikutnya")
            break
        
        time.sleep(delay)
    
    return data
        