-- 1. Mengambil data dari tabel utama Beasiswa
SELECT id, nama, deskripsi, logo, slug, periode_awal, periode_akhir, batas_daftar, jenis, kategori, status 
FROM beasiswa;

-- 2. Mengambil data dari tabel Syarat Beasiswa
SELECT id, beasiswa_id, syarat 
FROM beasiswa_syarat;

-- 3. Mengambil data dari tabel Benefit Beasiswa
SELECT id, beasiswa_id, benefit, icon 
FROM beasiswa_benefit;

-- 4. Mengambil data dari tabel Timeline Beasiswa
SELECT id, beasiswa_id, judul, tanggal_mulai, tanggal_selesai 
FROM beasiswa_timeline;

-- 5. Mengambil data dari tabel Tata Cara Pendaftaran Beasiswa
SELECT id, beasiswa_id, tata_cara, link 
FROM beasiswa_tata_cara;
