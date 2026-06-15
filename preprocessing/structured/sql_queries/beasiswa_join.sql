-- ========================================================
-- TAHAP DENORMALISASI BEASISWA (Menggunakan SQL JOIN)
-- ========================================================

SELECT 
    b.nama AS nama_beasiswa,
    b.deskripsi,
    b.periode_awal,
    b.periode_akhir,
    b.batas_daftar AS batas_pendaftaran,
    b.jenis AS jenis_beasiswa,
    b.kategori AS kategori_beasiswa,
    bs.syarat AS persyaratan,
    bb.benefit,
    bt.judul AS kegiatan_timeline,
    bt.tanggal_mulai AS tanggal_mulai_timeline,
    bt.tanggal_selesai AS tanggal_selesai_timeline,
    btc.tata_cara,
    btc.link AS link_tata_cara
FROM beasiswa b
LEFT JOIN beasiswa_syarat bs ON b.id = bs.beasiswa_id
LEFT JOIN beasiswa_benefit bb ON b.id = bb.beasiswa_id
LEFT JOIN beasiswa_timeline bt ON b.id = bt.beasiswa_id
LEFT JOIN beasiswa_tata_cara btc ON b.id = btc.beasiswa_id
WHERE b.slug = 'beasiswa-bank-negara-indonesia-bni-2026'; 
