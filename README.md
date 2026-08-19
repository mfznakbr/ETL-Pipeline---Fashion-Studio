# ETL Pipeline - Fashion Studio

## Project Overview

Project ini merupakan implementasi **ETL (Extract, Transform, Load) Pipeline** menggunakan Python sebagai bagian dari tugas akhir kelas **Belajar Fundamental Pemrosesan Data**.

Project ini menggunakan studi kasus analisis data produk kompetitor dari website **Fashion Studio**. Data produk diekstrak dari website, kemudian dilakukan proses transformasi dan pembersihan data agar memiliki kualitas yang lebih baik, sebelum akhirnya disimpan ke dalam repositori data dalam format CSV.

Pipeline ini dirancang menggunakan prinsip **modular programming**, dengan memisahkan setiap tahapan ETL ke dalam fungsi dan file Python yang berbeda. Selain itu, project juga menerapkan **unit testing** untuk memastikan fungsi-fungsi dalam pipeline dapat berjalan sesuai dengan yang diharapkan.

## Objectives

Tujuan dari project ini adalah:

- Mengimplementasikan proses **Extract, Transform, Load (ETL)** menggunakan Python.
- Mengambil data produk dari website Fashion Studio.
- Membersihkan dan mempersiapkan data agar siap digunakan untuk analisis lebih lanjut.
- Mengonversi harga produk dari USD ke Rupiah.
- Menghilangkan data duplikat, null, dan invalid.
- Menyimpan data hasil transformasi dalam format CSV.
- Menerapkan prinsip **modular code** pada pipeline.
- Melakukan **unit testing** terhadap fungsi-fungsi ETL.

## Data Source

Data diperoleh melalui proses web scraping dari website:

**Fashion Studio**  
https://fashion-studio.dicoding.dev

Website tersebut merupakan website fiktif yang digunakan khusus untuk kebutuhan pembelajaran dan submission.

Data produk yang diekstrak meliputi:

- `Title`
- `Price`
- `Rating`
- `Colors`
- `Size`
- `Gender`

Data diambil dari seluruh halaman yang tersedia pada website sesuai dengan ketentuan project.

## ETL Pipeline

Pipeline terdiri dari tiga tahapan utama:

### 1. Extract

Tahap **Extract** bertujuan untuk mengambil data produk dari website Fashion Studio menggunakan teknik web scraping.

Data yang dikumpulkan meliputi informasi:

- Nama produk
- Harga
- Rating
- Jumlah warna
- Ukuran
- Gender

Data dari beberapa halaman website dikumpulkan dan digabungkan menjadi satu dataset untuk diproses pada tahap berikutnya.

### 2. Transform

Tahap **Transform** bertujuan untuk meningkatkan kualitas dan konsistensi data yang telah diperoleh.

Beberapa proses transformasi yang dilakukan meliputi:

- Membersihkan data yang tidak valid.
- Menghapus data duplikat.
- Menangani nilai null.
- Menghapus data dengan informasi yang tidak valid seperti `Unknown Product`.
- Mengonversi harga dari USD ke Rupiah.
- Menggunakan asumsi nilai tukar:

```text
1 USD = Rp16.000
