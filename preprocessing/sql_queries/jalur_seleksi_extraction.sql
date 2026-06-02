-- 1. Mengambil data dari tabel utama Jalur Seleksi
SELECT id, nama, banner, slug, deskripsi, biaya_daftar, is_active, periode_id 
FROM jalur_seleksi;

-- 2. Mengambil data dari tabel Persyaratan Umum
SELECT id, jalur_id, persyaratan 
FROM persyaratan_umum;

-- 3. Mengambil data dari tabel Cara Pendaftaran
SELECT id, jalur_id, deskripsi 
FROM cara_pendaftaran;

-- 4. Mengambil data dari tabel Dokumen Pendaftaran
SELECT id, jalur_id, dokumen 
FROM dokumen_pendaftaran;

-- 5. Mengambil data dari tabel Jadwal Pendaftaran
SELECT id, jalur_id, periode_id, tanggal_mulai, tanggal_selesai, type 
FROM jadwal_pendaftaran;

-- 6. Mengambil data dari tabel Master Periode
SELECT id, nama, tanggal_mulai, tanggal_selesai 
FROM periode;
