-- ========================================================
-- TAHAP DENORMALISASI JALUR SELEKSI (Menggunakan SQL JOIN)
-- ========================================================

SELECT 
    js.nama AS nama_jalur_seleksi,
    js.biaya_daftar,
    js.deskripsi,
    p.nama AS nama_periode,
    p.tanggal_mulai AS periode_mulai,
    p.tanggal_selesai AS periode_selesai,
    pu.persyaratan,
    cp.deskripsi AS cara_pendaftaran,
    dp.dokumen AS dokumen_pendaftaran,
    jp.tanggal_mulai AS jadwal_mulai,
    jp.tanggal_selesai AS jadwal_selesai,
    jp.type AS tipe_jadwal
FROM jalur_seleksi js
LEFT JOIN periode p ON js.periode_id = p.id
LEFT JOIN persyaratan_umum pu ON js.id = pu.jalur_id
LEFT JOIN cara_pendaftaran cp ON js.id = cp.jalur_id
LEFT JOIN dokumen_pendaftaran dp ON js.id = dp.jalur_id
LEFT JOIN jadwal_pendaftaran jp ON js.id = jp.jalur_id
WHERE js.slug = 'pmdk'; -- Ganti dengan 'pmdk', 'odt', 'tka', 'snbt', 'rpl', atau 'magister'
