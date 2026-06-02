-- ================================================================
-- AUTO-GENERATED SQL INSERT STATEMENTS
-- Sumber: data/structured/ (JSON files)
-- Target: Database pmb_itenas
-- Generated: 2026-05-30 19:41:41
-- ================================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
USE `pmb_itenas`;


-- ============================================
-- BEASISWA (dari data/structured/beasiswa/)
-- ============================================

-- [1] Beasiswa Bank Negara Indonesia (BNI) 2026
INSERT INTO `beasiswa` (`id`, `nama`, `deskripsi`, `logo`, `slug`, `periode_awal`, `periode_akhir`, `batas_daftar`, `jenis`, `kategori`, `status`, `created_at`, `updated_at`) VALUES
  (1, 'Beasiswa Bank Negara Indonesia (BNI) 2026', 'Beasiswa BNI adalah program bantuan pendidikan dari Bank Negara Indonesia untuk mahasiswa berprestasi (IPK min. 3,00) yang kurang mampu secara finansial, mencakup pembebasan biaya kuliah atau bantuan tunai. Program ini sering ditargetkan pada mahasiswa semester aktif (2-8) di universitas mitra.', '', 'beasiswa-bank-negara-indonesia-bni-2026', '2026-06-28', '2026-07-05', '2026-07-05', '1', '1', '1', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Syarat Beasiswa ID=1
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (1, 'Surat Permohonan Beasiswa yang ditujukan kepada Rektor Itenas (https://kemahasiswaan.itenas.ac.id/wp-content/uploads/2024/06/Surat-Permohonan-Beasiswa-ITENAS.BKAF_MHS_BSW01.docx)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (1, 'Mengisi Biodata pengajuan Beasiswa (https://kemahasiswaan.itenas.ac.id/wp-content/uploads/2024/06/Biodata-Pengajuan-ITENAS.BKAF_MHS_BSW02-1.docx)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (1, 'Menyerahkan fotocopy Kartu Tanda Mahasiswa (KTM) dan Kartu Rencana Studi Mahasiswa (KRS) sebagai bukti mahasiswa aktif dan terdaftar di semester genap 2025/2026.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (1, 'Melampirkan Surat Pernyataan tidak sedang menerima beasiswa dari sumber lain (https://kemahasiswaan.itenas.ac.id/wp-content/uploads/2023/05/Surat-Pernyataan-Tidak-Menerima-Beasiswa-Lain-ITENAS.BKAF_MHS_BSW03.doc-1-2-2.docx)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (1, 'Menyertakan Transkrip Nilai dengan IPK minimum 3,00 dan disahkan pimpinan Program Studi, Transkrip Nilai dapat diprint di Portal Mahasiswa di menu Inguiry Point B (Nilai Semester).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (1, 'Melampirkan Surat Keterangan perincian gaji/penghasilan orangtua perbulan yang ditandatangani oleh pejabat berwenang, sedangkan untuk wiraswasta / wirausaha dapat mengisi form (https://kemahasiswaan.itenas.ac.id/wp-content/uploads/2023/05/Surat-Pernyatan-Penghasilan-Wiraswasta-ITENAS.BKAF_MHS_BSW06-1.doc)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (1, 'Menyerahkan fotocopy Kartu Tanda Penduduk (KTP)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (1, 'Menyerahkan fotocopy Kartu Keluarga.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (1, 'Melampirkan fotocopy sertifikat, piagam penghargaan atau bukti prestasi lainnya (ko-kurikuler dan atau ekstra kurikuler).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (1, 'Menyerahkan Pas photo terbaru berwarna ukuran 3×', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (1, 'Surat keterangan Tidak Mampu (SKTM) yang dikeluarkan oleh kelurahan/desa.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Benefit Beasiswa ID=1
INSERT INTO `beasiswa_benefit` (`beasiswa_id`, `benefit`, `icon`, `created_at`, `updated_at`) VALUES
  (1, 'Bantuan biaya pendidikan kuliah per semester di kampus', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_benefit` (`beasiswa_id`, `benefit`, `icon`, `created_at`, `updated_at`) VALUES
  (1, 'Dana tunjangan bulanan untuk kebutuhan hidup sehari-hari selama masa studi.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_benefit` (`beasiswa_id`, `benefit`, `icon`, `created_at`, `updated_at`) VALUES
  (1, 'Dukungan dana untuk menunjang kebutuhan literatur dan referensi akademik.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Timeline Beasiswa ID=1
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (1, 'Masa Pendaftaran Beasiswa BNI 2026', '2026-06-28', '2026-07-12', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Tata Cara Beasiswa ID=1
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (1, 'Pendaftaran beasiswa ini dilakukan secara online. Berkas yang tidak lengkap tidak akan kami proses. Format Berkas PDF kecuali Pas Photo.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (1, 'Berkas yang tidak lengkap tidak akan kami proses. Format Berkas PDF kecuali Pas Photo.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (1, 'Berkas yang membutuhkan tanda tangan pejabat (Ketua Program Studi, Dekan, Kepala Biro BKA) dikosongkan saja dan langsung upload karena tanda tangan pejabat akan dikolektifkan oleh Biro Kemahasiswaan dan Alumni apabila mahasiswa lolos seleksi beasiswa.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- [2] Beasiswa Kartu Indonesia Pintar (KIP-K) Itenas 2026
INSERT INTO `beasiswa` (`id`, `nama`, `deskripsi`, `logo`, `slug`, `periode_awal`, `periode_akhir`, `batas_daftar`, `jenis`, `kategori`, `status`, `created_at`, `updated_at`) VALUES
  (2, 'Beasiswa Kartu Indonesia Pintar (KIP-K) Itenas 2026', 'Pemerintah Indonesia terus berkomitmen untuk fokus meningkatkan pembangunan Sumberdaya Manusia melalui berbagai upaya cerdas. Kartu Indonesia Pintar Kuliah (KIP-Kuliah) adalah salah satu upaya untuk membantu asa para siswa yang memiliki keterbatasan ekonomi tetapi berprestasi untuk melanjutkan studi di perguruan tinggi.', '', 'beasiswa-kartu-indonesia-pintar-kip-k-itenas-2026', '2026-07-01', '2026-09-01', '2026-08-01', '0', '1', '1', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Syarat Beasiswa ID=2
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (2, 'Siswa MA/SMA/SMK Tahun Lulusan 2025 & 2026', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (2, 'Siswa telah mempunyai kartu KIP-K dan terdaftar Data Terpadu Kesejahteraan Sosial (DTKS)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (2, 'Mempunyai no pendaftaran KIP-K yang didapatkan setelah daftar pada laman : http://kip-kuliah.kemdikbud.go.id', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (2, 'Mendaftarkan Program Studi (Prodi harus sesuai dengan yang dipilih pada laman : http://kip-kuliah.kemdikbud.go.id)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (2, 'Melampirkan bukti gaji orang tua yang sudah di tanda tangani', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (2, 'Melampirkan foto depan rumah dengan keluarga', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (2, 'Melampirkan bukti tagihan listrik.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Benefit Beasiswa ID=2
INSERT INTO `beasiswa_benefit` (`beasiswa_id`, `benefit`, `icon`, `created_at`, `updated_at`) VALUES
  (2, 'Bantuan biaya pendidikan  penuh selama masa studi 4 tahun.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_benefit` (`beasiswa_id`, `benefit`, `icon`, `created_at`, `updated_at`) VALUES
  (2, 'Bantuan biaya hidup bulanan', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Timeline Beasiswa ID=2
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (2, 'Pendaftaran KIPK Itenas', '2026-07-08', '2026-07-22', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Tata Cara Beasiswa ID=2
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (2, 'Proses pendaftaran dilakukan secara online pada laman http://kip-k.itenas.ac.id/', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- [3] Beasiswa Mandiri Inhealth 2026
INSERT INTO `beasiswa` (`id`, `nama`, `deskripsi`, `logo`, `slug`, `periode_awal`, `periode_akhir`, `batas_daftar`, `jenis`, `kategori`, `status`, `created_at`, `updated_at`) VALUES
  (3, 'Beasiswa Mandiri Inhealth 2026', 'Mandiri Inhealth adalah perusahaan asuransi jiwa dan kesehatan dengan jaminan kesehatan komersial untuk perusahaan swasta, BUMN, dan institusi pemerintahan. Dalam rangka memotivasi mahasiswa untuk meningkatkan prestasi akademik dan menyelesaikan Pendidikan Tinggi, Mandiri Inhealth melaksanakan program kemitraan yaitu Mandiri Inhealth', '', 'beasiswa-mandiri-inhealth-2026', '2026-03-21', '2026-09-14', '2026-04-04', '1', '1', '1', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Syarat Beasiswa ID=3
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (3, 'Persyaratan untuk dapat mengikuti Beasiswa Mandiri Inhealth:', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (3, 'Mengisi Surat Permohonan Beasiswa (https://kemahasiswaan.itenas.ac.id/wp-content/uploads/2023/03/Surat-Permohonan-Beasiswa-ITENAS.BKAF_MHS_BSW01.docx)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (3, 'Mengisi Biodata pengajuan Beasiswa (https://kemahasiswaan.itenas.ac.id/wp-content/uploads/2023/03/Biodata-Pengajuan-ITENAS.BKAF_MHS_BSW02.docx) setelah pengisian kemudian diupload*.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (3, 'Upload/Unggah Kartu Tanda Mahasiswa (KTM) dan Kartu Rencana Studi Mahasiswa (KRS) sebagai bukti mahasiswa aktif (Angkatan 2021 & 2022) dan terdaftar di semester Genap 2022/2023.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (3, 'Melampirkan Surat Pernyataan tidak sedang menerima beasiswa dari sumber lain (https://kemahasiswaan.itenas.ac.id/wp-content/uploads/2023/03/Surat-Pernyataan-Tidak-Menerima-Beasiswa-Lain-ITENAS.BKAF_MHS_BSW03.doc-1-2.docx), setelah dilakukan pengisian kemudian diupload*.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (3, 'Upload/Unggah Transkrip Nilai dengan IPK minimum 2.75, Transkrip Nilai dapat diprint di Portal Mahasiswa pada menu Inquiry Point B (Nilai Semester).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (3, 'Melampirkan Surat Keterangan perincian gaji/penghasilan orang tua perbulan yang ditandatangani oleh pejabat berwenang, sedangkan untuk wiraswasta / wirausaha dapat mengisi form (https://kemahasiswaan.itenas.ac.id/wp-content/uploads/2023/03/Surat-Pernyatan-Penghasilan-Wiraswasta-ITENAS.BKAF_MHS_BSW06-1.doc)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (3, 'Bagi Calon penerima beasiswa, aktif dalam kegiatan kemahasiswaan dilengkapi bukti dokumen keaktifan. Upload/Unggah.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (3, 'Upload/Unggah sertifikat, piagam penghargaan atau bukti prestasi lainnya (ko-kurikuler dan atau ekstra kurikuler).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Benefit Beasiswa ID=3
INSERT INTO `beasiswa_benefit` (`beasiswa_id`, `benefit`, `icon`, `created_at`, `updated_at`) VALUES
  (3, 'Pengurangan 50% Uang Kuliah Tetap (UKT) Semester Ganjil 2026/2027', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Timeline Beasiswa ID=3
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (3, 'Pendaftaran Beasiswa Mandiri Inhealth', '2026-03-21', '2026-04-04', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (3, 'Pengumuman Hasil', '2026-09-14', '2026-09-14', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Tata Cara Beasiswa ID=3
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (3, 'Pendaftaran beasiswa ini dilakukan secara online.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (3, 'Format Berkas PDF kecuali Pas Photo. Berkas yang tidak lengkap tidak akan kami proses.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (3, 'Berkas yang membutuhkan tanda tangan pejabat (Ketua Program Studi, Dekan, Kepala Biro BKA) dikosongkan saja dan langsung upload karena tanda tangan pejabat akan dikolektifkan oleh Biro Kemahasiswaan dan Alumni apabila mahasiswa lolos seleksi beasiswa', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (3, 'Untuk informasi lebih lanjut dapat menghubungi Biro Kemahasiswaan dan Alumni. Instagram: kemahasiswaan.itenas', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- [4] Beasiswa PT. TKG Taekwang Indonesia
INSERT INTO `beasiswa` (`id`, `nama`, `deskripsi`, `logo`, `slug`, `periode_awal`, `periode_akhir`, `batas_daftar`, `jenis`, `kategori`, `status`, `created_at`, `updated_at`) VALUES
  (4, 'Beasiswa PT. TKG Taekwang Indonesia', 'PT. TKG Taekwang Indonesia adalah perusahaan manufaktur sepatu merk terkenal yang berasal dari Korea Selatan dengan luas lahan 45 Hektar dengan jumlah karyawan tetap sekitar 34.000 orang yang terletak di Kabupaten Subang, Jawa Barat.', '', 'beasiswa-pt-tkg-taekwang-indonesia', '2026-03-02', '2026-03-09', '2026-03-09', '1', '1', '1', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Syarat Beasiswa ID=4
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (4, 'Mahasiswa yang akan lulus pada tahun 2026', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (4, 'Tingkat S1/D4 jurusan Teknik Industri, Teknik Sipil dan Teknik Lingkungan', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (4, 'IPK minimal 3,0 per semester', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (4, 'Bersedia melampirkan transkrip nilai sah', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (4, 'Tanpa Kerja magang di perusahaan', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (4, 'Bersedia menerima serta mengikuti undangan dari perusahaan', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (4, 'Melampirkan CV (termasuk foto diri) dan transkrip nilai terakhir menggunakan link google drive', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (4, 'Taat dan patuh terhadap peraturan Universitas/Kampus serta perjanjian Beasiswa', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Benefit Beasiswa ID=4
INSERT INTO `beasiswa_benefit` (`beasiswa_id`, `benefit`, `icon`, `created_at`, `updated_at`) VALUES
  (4, 'Biaya kuliah dan bantuan biaya hidup untuk 2 semester', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Timeline Beasiswa ID=4
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (4, 'Masa Pendaftaran Beasiswa PT. TKG Taekwang Indonesia 2026', '2026-03-02', '2026-03-09', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- [5] Beasiswa Rawan Melanjutkan Pendidikan (RMP) Tahun 2026
INSERT INTO `beasiswa` (`id`, `nama`, `deskripsi`, `logo`, `slug`, `periode_awal`, `periode_akhir`, `batas_daftar`, `jenis`, `kategori`, `status`, `created_at`, `updated_at`) VALUES
  (5, 'Beasiswa Rawan Melanjutkan Pendidikan (RMP) Tahun 2026', 'Beasiswa RMP merupakan beasiswa bagi mahasiswa Rawan Melanjutkan Pendidikan (RMP) yang diberikan oleh Walikota Bandung.', '', 'beasiswa-rawan-melanjutkan-pendidikan-rmp-tahun-2026', '2026-04-26', '2026-05-10', '2026-05-10', '1', '1', '1', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Syarat Beasiswa ID=5
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (5, 'Persyaratan untuk dapat mengikuti Beasiswa RMP Tahun 2025, sebagai berikut:', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (5, 'Mengisi surat pengajuan Beasiswa (https://kemahasiswaan.itenas.ac.id/wp-content/uploads/2023/08/Surat-Permohonan-Beasiswa-ITENAS.BKAF_MHS_BSW01-1.docx) setelah pengisian kemudian diupload.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (5, 'Upload fotocopy Kartu Tanda Mahasiswa (KTM) dan Kartu Rencana Studi Mahasiswa (KRS) sebagai bukti mahasiswa aktif dan terdaftar di semester genap 2023/2024.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (5, 'Melampirkan Surat Pernyataan tidak sedang menerima beasiswa dari sumber lain (https://kemahasiswaan.itenas.ac.id/wp-content/uploads/2022/11/Surat-Pernyataan-Tidak-Menerima-Beasiswa-Lain-ITENAS.BKAF_MHS_BSW03.doc-1-2.docx), setelah dilakukan pengisian kemudian diupload.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (5, 'Menyertakan Transkrip Nilai dengan IPK minimum 2.50, Transkrip Nilai dapat diprint di Portal Mahasiswa di menu Inquiry Point B (Nilai Semester).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (5, 'Upload KTP & Kartu Keluarga (Domisili Kota bandung)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (5, 'Upload Pas Foto terbaru berwarna ukuran 3 x 4 cm', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (5, 'Mahasiswa terdata di Data Terpadu Kesejahteraan Sosial (DTKS), yang dapat di cek melalui Hotline Dinsos Kota Bandung', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (5, 'Semua dokumen persyaratan discan terlebih dahulu selanjutnya dikirim dalam bentuk pdf diupload ke https://bit.ly/BeasiswaRMP_Itenas', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Benefit Beasiswa ID=5
INSERT INTO `beasiswa_benefit` (`beasiswa_id`, `benefit`, `icon`, `created_at`, `updated_at`) VALUES
  (5, 'Subsidi Biaya Pendidikan: Bantuan langsung digunakan untuk membayar atau mengurangi beban DPP/SPP di perguruan tinggi mitra.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Timeline Beasiswa ID=5
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (5, 'Masa Pendaftaran Beasiswa RMP 2026', '2026-04-26', '2026-05-10', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Tata Cara Beasiswa ID=5
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (5, 'Pendaftaran beasiswa ini dilakukan secara online.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (5, 'Format Berkas PDF. Berkas yang tidak lengkap tidak akan kami proses.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (5, 'Berkas yang membutuhkan tanda tangan pejabat diabaikan dan langsung upload karena tanda tangan pejabat akan dikolektifkan oleh Biro Kemahasiswaan dan Alumni.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (5, 'Untuk informasi lebih lanjut dapat menghubungi Biro Kemahasiswaan dan Alumni. Instagram: kemahasiswaan.itenas', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- [6] Jabar Future Leaders Scholarship (JFLS) 2026
INSERT INTO `beasiswa` (`id`, `nama`, `deskripsi`, `logo`, `slug`, `periode_awal`, `periode_akhir`, `batas_daftar`, `jenis`, `kategori`, `status`, `created_at`, `updated_at`) VALUES
  (6, 'Jabar Future Leaders Scholarship (JFLS) 2026', 'Diberitahukan Kepada Mahasiswa Institut Teknologi Nasional Bandung, bahwa Pemerintah Provinsi Jawa Barat membuka kesempatan untuk mahasiswa S1 mendapatkan Beasiswa Jabar Future Leaders. Beasiswa JFLS  merupakan salah satu program unggulan Pemerintah Provinsi Jawa Barat yang tujuannya untuk memberikan beasiswa pendidikan kepada masyarakat Jawa Barat yang sedang menempuh pendidikan tinggi jenjang D3, D4, S1, S2, dan S3 yang berprestasi baik dalam bidang akademik maupun non-akademik.', '', 'jabar-future-leaders-scholarship-jfls-2026', '2026-06-20', '2026-11-30', '2026-07-20', '1', '1', '1', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Syarat Beasiswa ID=6
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (6, 'Maksimal batas tahun kelulusan dari SMA/SMK sederajat tiga tahun terakhir;', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (6, 'Melampirkan nilai USBN, dan jika ada SNBT, batas rata-rata nilai adalah 7,0 skala 10 atau 70,0 skala 100 (untuk mahasiswa Baru Itenas Angkatan 2023)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (6, 'Memiliki surat keterangan diterima dari perguruan tinggi yang telah ditentukan.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (6, 'Melampirkan transkrip nilai dengan IPK minimal 3,0 skala 4,0 (Untuk Mahasiswa Berjalan angkatan 2021, 2022, dan 2023 ). dapat diprint di Portal Mahasiswa di menu Inguiry Point B (Nilai Semester). Setelah diprint di scan, selanjutnya dikirim ke email Ketua Program Studi untuk ditandatangani.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (6, 'Memiliki motivasi untuk kuliah', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Benefit Beasiswa ID=6
INSERT INTO `beasiswa_benefit` (`beasiswa_id`, `benefit`, `icon`, `created_at`, `updated_at`) VALUES
  (6, 'Uang pendidikan sebesar Rp. 8.000.000,- (Delapan Juta Rupiah) dan/atau Beasiswa pendidikan penuh selama 4 tahunUang pendidikan sebesar Rp. 8.000.000,- (Delapan Juta Rupiah) dan/atau Beasiswa pendidikan penuh selama 4 tahun', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Timeline Beasiswa ID=6
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (6, 'Masa Pendaftaran Beasiswa JFLS 2026', '2026-06-20', '2026-07-20', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (6, 'Seleksi Administrasi', '2026-07-24', '2026-08-9', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (6, 'Verifikasi Perguruan Tinggi', '2026-08-14', '2026-08-23', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (6, 'Seleksi Pemprov Jabar', '2026-08-28', '2026-09-06', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (6, 'Pengumuman Penerima', '2026-09-25', '2026-09-25', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (6, 'Pencairan Dana Beasiswa', '2026-10-31', '2026-11-30', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- [7] Online Scholarship Competition (OSC) S1
INSERT INTO `beasiswa` (`id`, `nama`, `deskripsi`, `logo`, `slug`, `periode_awal`, `periode_akhir`, `batas_daftar`, `jenis`, `kategori`, `status`, `created_at`, `updated_at`) VALUES
  (7, 'Online Scholarship Competition (OSC) S1', 'Online Scholarship Competition (OSC) adalah kompetisi beasiswa online pertama di Indonesia yang diselenggarakan sejak 2015 oleh Surya Edukasi Bangsa Foundation bersama Medcom.id. Program ini membuka akses beasiswa S1 dan S2 di perguruan tinggi favorit melalui kolaborasi dengan perguruan tinggi swasta, guna mendukung pemerataan pendidikan dan pengembangan SDM unggul bagi putra-putri Indonesia dari berbagai latar belakang.', '', 'online-scholarship-competition-osc-s1', '2026-08-21', '2026-11-12', '2026-11-12', '0', '1', '1', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Syarat Beasiswa ID=7
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (7, 'Setiap peserta OSC S1 diwajibkan untuk mengetahui semua syarat yang berlaku, diantaranya :', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (7, 'Mengisi formulir data diri lengkap dan melakukan pembayaran registrasi sebesar Rp. 35.000,- di https://osc.medcom.id/', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (7, 'Siswa/i SMA/SMK/MA Sederajat & Santri yang duduk di kelas 3/XII, dan akan lulus di 2027', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (7, 'Siswa/i SMA/SMK/MA Sederajat & Santri yang telah lulus di 2026 dan Tahun 2026, tapi belum kuliah (Gapyear)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (7, 'Siswa/i tidak pernah menerima program beasiswa dari lembaga beasiswa lainnya', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (7, 'Memiliki prestasi akademik dan atau non akademik', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (7, 'Memiliki keinginan kuliah yang kuat / tinggi', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (7, 'Mengupload twibbon peserta Beasiswa OSC 2026 ke Instagram dan tag ke @beasiswaosc', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (7, 'Follow akun sosial media : Instagram dan Twitter @BeasiswaOSC, Instagram dan Twitter @medcomid, dan Instagram @suryaedukasibangsa', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Benefit Beasiswa ID=7
INSERT INTO `beasiswa_benefit` (`beasiswa_id`, `benefit`, `icon`, `created_at`, `updated_at`) VALUES
  (7, 'Bantuan biaya pendidikan penuh selama masa studi 4 tahun.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_benefit` (`beasiswa_id`, `benefit`, `icon`, `created_at`, `updated_at`) VALUES
  (7, 'Mahasiswa dari luar daerah memperoleh bantuan biaya hidup sesuai ketentuan.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Timeline Beasiswa ID=7
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (7, 'Pembukaan Pendaftaran Beasiswa OSC S1 dan Beasiswa OSC S2 2025', '2026-08-21', '2026-11-12', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (7, 'Pelaksanaan Tryout Wajib Peserta', '2026-09-07', '2026-09-08', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (7, 'Tahap seleksi I Online Test', '2026-09-15', '2026-09-15', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (7, 'Pengumuman hasil tahap seleksi I Online Test', '2026-09-21', '2026-09-21', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (7, 'Pengumuman persiapan berkas', '2026-09-21', '2026-09-21', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (7, 'Tahap Seleksi II Final Test', '2026-09-21', '2026-12-05', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (7, 'OSC Awards', '2026-12-19', '2026-12-19', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Tata Cara Beasiswa ID=7
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (7, 'Setelah mengisi data diri dengan lengkap, peserta hanya diperbolehkan memilih 1 dari universitas yang tersedia', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (7, 'Peserta dapat memilih 2 program studi (prodi) dari 1 universitas yang dipilih (pilihan universitas & prodi TIDAK BISA diubah). Pilihan pertama peserta, akan dianggap sebagai prioritas utama peserta dalam pemilihan prodi', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (7, 'Peserta WAJIB mengikuti Try Out OSC secara online menggunakan voucher free Tryout yang sudah termasuk dalam pendaftaranPeserta WAJIB mengikuti ONLINE TEST yang telah ditentukan waktunya. Peserta WAJIB menjawab semua soal test yang tersedia, sesuai dengan batas waktu yang telah ditentukan. Peserta yang lolos tahap pertama online test, WAJIB mengikuti tahap FINAL TEST', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (7, 'Untuk peserta yang lolos ke tahap FINAL TEST WAJIB mengirimkan berkas sebagai berikut: Form data diri beasiswa OSC (download di laman profil kampus tujuan). Pas foto ukuran 4x6 dengan warna latar belakang sesuai tahun lahir. Scan raport kelas 10 dan 11 (untuk gap year sertakan juga scan raport kelas 12). Scan surat pengantar dari sekolah (untuk kelas 12) dan ijazah SMA/SMK/MA Sederajat & Pesantren/Boarding School (untuk gap year). Scan sertifikat / piagam penghargaan akademik dan non akademik (bila ada). Portofolio karya berupa karya tulis / foto / design / dll (bila ada)', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (7, 'Peserta yang TIDAK MENGIKUTI Final Test beasiswa OSC, akan dinyatakan GUGUR. Peserta WAJIB mengikuti seluruh proses atau tahapan yang ada di beasiswa OSC', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- [8] Online Scholarship Competition (OSC) S2
INSERT INTO `beasiswa` (`id`, `nama`, `deskripsi`, `logo`, `slug`, `periode_awal`, `periode_akhir`, `batas_daftar`, `jenis`, `kategori`, `status`, `created_at`, `updated_at`) VALUES
  (8, 'Online Scholarship Competition (OSC) S2', 'Online Scholarship Competition (OSC) S2 adalah program beasiswa pascasarjana online yang diselenggarakan oleh Surya Edukasi Bangsa Foundation bersama Medcom.id. Program ini bekerja sama dengan 11 perguruan tinggi swasta ternama di 5 kota dan menyediakan 80 beasiswa S2 bagi tenaga pendidik dan masyarakat umum, dengan proses pendaftaran dan seleksi awal dilakukan secara online untuk mendukung peningkatan kualitas SDM Indonesia.', '', 'online-scholarship-competition-osc-s2', '2026-08-21', '2026-11-12', '2026-11-12', '0', '1', '1', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Syarat Beasiswa ID=8
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (8, 'Syarat Kepesertaan Beasiswa OSC S2', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (8, 'Warga negara Indonesia (WNI)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (8, 'Terbuka untuk Tenaga Pengajar dan Umum', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (8, 'Tidak ada minimal dan maksimal usia', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (8, 'Minimal IPK S1 3.0', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (8, 'Alumnus program S1 dari perguruan tinggi terakreditasi', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (8, 'Pendaftar tidak sedang mendaftar, menerima, atau akan menerima beasiswa lain', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (8, 'Melengkapi profil pendaftaran di laman osc.medcom.id', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_syarat` (`beasiswa_id`, `syarat`, `created_at`, `updated_at`) VALUES
  (8, 'Memiliki motivasi untuk kuliah', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Benefit Beasiswa ID=8
INSERT INTO `beasiswa_benefit` (`beasiswa_id`, `benefit`, `icon`, `created_at`, `updated_at`) VALUES
  (8, 'Bantuan biaya pendidikan penuh selama masa studi 4 tahun.', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Timeline Beasiswa ID=8
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (8, 'Masa Pendaftaran Beasiswa OSC S2', '2026-08-21', '2026-11-12', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (8, 'Pelaksanaan Tryout Wajib Peserta', '2026-11-07', '2026-11-08', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (8, 'Tahap seleksi I Online Test', '2026-11-15', '2026-11-15', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (8, 'Pengumuman hasil tahap seleksi I Online Test', '2026-11-21', '2026-11-21', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (8, 'Pengumuman persiapan berkas', '2026-11-21', '2026-11-21', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (8, 'Tahap Seleksi II Final Test', '2026-11-21', '2026-12-05', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_timeline` (`beasiswa_id`, `judul`, `tanggal_mulai`, `tanggal_selesai`, `created_at`, `updated_at`) VALUES
  (8, 'OSC Awards', '2026-12-19', '2026-12-19', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Tata Cara Beasiswa ID=8
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (8, 'Setelah mengisi data diri dengan lengkap, peserta wajib melakukan pembayaran pendaftaran sebesar Rp 150.000 (Sebagian uang pendaftaran akan didonasikan kepada Surya Edukasi Bangsa Foundation)', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (8, 'Peserta hanya diperbolehkan memilih 1 dari universitas yang tersedia dan memilih 2 program studi dari universitas yang dipilih (pilihan universitas & prodi TIDAK BISA diubah). Pilihan pertama peserta, akan dianggap sebagai prioritas utama peserta dalam pemilihan prodi', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (8, 'Peserta WAJIB mengikuti Try Out OSC secara online menggunakan voucher free Tryout yang sudah termasuk dalam pendaftaran. Peserta WAJIB mengikuti ONLINE TEST yang telah ditentukan waktunya. Peserta WAJIB menjawab semua soal test yang tersedia, sesuai dengan batas waktu yang telah ditentukan. Peserta yang lolos, WAJIB mengikuti tahap FINAL TEST', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (8, 'Untuk peserta yang lolos ke tahap FINAL TEST WAJIB mengirimkan berkas sebagai berikut: Form data diri beasiswa OSC S2 (download di laman profil kampus tujuan). Pas foto ukuran 4x6 dengan warna latar belakang sesuai tahun lahir. Scan Ijazah atau SKL. Scan transkrip nilai S1. Scan sertifikat / piagam penghargaan akademik dan non akademik (bila ada). Portofolio karya berupa karya tulis / foto / design / dll (bila ada)', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `beasiswa_tata_cara` (`beasiswa_id`, `tata_cara`, `link`, `created_at`, `updated_at`) VALUES
  (8, 'Peserta yang TIDAK MENGIKUTI Final Test beasiswa OSC, akan dinyatakan GUGUR. Peserta WAJIB mengikuti seluruh proses atau tahapan yang ada di beasiswa OSC S2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');


-- ============================================
-- BIAYA PENDIDIKAN (dari data/structured/biaya/)
-- ============================================

-- Biaya: Arsitektur
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Arsitektur', '0', 'UKT: Rp 2.500.000; SKS: 19 x Rp 300.000; Praktikum: Rp 400.000; DPP: Rp 15.000.000', '23600000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Arsitektur', '1', 'UKT: Rp 2.500.000; SKS: 18 x Rp 300.000; Praktikum: Rp 400.000', '8300000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Arsitektur (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; Jalur Rekognisi Pembelajaran Lampau (RPL)', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Desain Interior
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Desain Interior', '0', 'UKT: Rp 2.500.000; SKS: 20 x Rp 350.000; Praktikum: Rp 600.000; DPP: Rp 15.000.000', '25100000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Desain Interior', '1', 'UKT: Rp 2.500.000; SKS: 16 x Rp 350.000; Praktikum: Rp 450.000', '8550000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Desain Interior (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; Jalur Rekognisi Pembelajaran Lampau (RPL)', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Desain Komunikasi Visual
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Desain Komunikasi Visual', '0', 'UKT: Rp 2.500.000; SKS: 18 x Rp 350.000; Praktikum: Rp 720.000; DPP: Rp 17.500.000', '27020000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Desain Komunikasi Visual', '1', 'UKT: Rp 2.500.000; SKS: 18 x Rp 350.000; Praktikum: Rp 720.000', '9520000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Desain Komunikasi Visual (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; Jalur Rekognisi Pembelajaran Lampau (RPL)', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Desain Produk
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Desain Produk', '0', 'UKT: Rp 2.500.000; SKS: 20 x Rp 350.000; Praktikum: Rp 480.000; DPP: Rp 15.000.000', '24980000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Desain Produk', '1', 'UKT: Rp 2.500.000; SKS: 18 x Rp 350.000; Praktikum: Rp 600.000', '9400000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Desain Produk (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; Jalur Rekognisi Pembelajaran Lampau (RPL)', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Informatika
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Informatika', '0', 'UKT: Rp 2.500.000; SKS: 18 x Rp 350.000; DPP: Rp 17.500.000', '26300000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Informatika', '1', 'UKT: Rp 2.500.000; SKS: 18 x Rp 350.000', '8800000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Informatika (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; Jalur Rekognisi Pembelajaran Lampau (RPL)', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Perencanaan Wilayah dan Kota
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Perencanaan Wilayah dan Kota', '0', 'UKT: Rp 2.500.000; SKS: 20 x Rp 300.000; Praktikum: Rp 300.000; DPP: Rp 12.500.000', '21300000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Perencanaan Wilayah dan Kota', '1', 'UKT: Rp 2.500.000; SKS: 18 x Rp 300.000; Praktikum: Rp 650.000', '8550000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Perencanaan Wilayah dan Kota (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; Jalur Rekognisi Pembelajaran Lampau (RPL)', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Sistem Informasi
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Sistem Informasi', '0', 'UKT: Rp 2.500.000; SKS: 18 x Rp 300.000; DPP: Rp 12.500.000', '20400000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Sistem Informasi', '1', 'UKT: Rp 2.500.000; SKS: 18 x Rp 300.000', '7900000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Sistem Informasi (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; Jalur Rekognisi Pembelajaran Lampau (RPL)', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Teknik Elektro
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Elektro', '0', 'UKT: Rp 2.500.000; SKS: 18 x Rp 300.000; Praktikum: Rp 250.000; DPP: Rp 12.500.000', '20650000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Elektro', '1', 'UKT: Rp 2.500.000; SKS: 18 x Rp 300.000; Praktikum: Rp 250.000', '8150000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Elektro (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; Jalur Rekognisi Pembelajaran Lampau (RPL)', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Teknik Geodesi
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Geodesi', '0', 'UKT: Rp 2.500.000; SKS: 20 x Rp 350.000; Praktikum: Rp 140.000; DPP: Rp 12.500.000', '22140000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Geodesi', '1', 'UKT: Rp 2.500.000; SKS: 19 x Rp 350.000; Praktikum: Rp 140.000', '9290000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Geodesi (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; Jalur Rekognisi Pembelajaran Lampau (RPL)', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Teknik Industri
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Industri', '0', 'UKT: Rp 2.500.000; SKS: 19 x Rp 350.000; Praktikum: Rp 195.000; DPP: Rp 15.000.000', '24345000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Industri', '1', 'UKT: Rp 2.500.000; SKS: 18 x Rp 350.000', '8800000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Industri (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; ', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Industri S2 (Semester 1)', '0', 'UKT: Rp 3.000.000; SKS: 12 x Rp 700.000', '0', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Industri S2 (Semester 2)', '1', 'UKT: Rp 3.000.000; SKS: 12 x Rp 700.000', '0', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Industri S2 (Semester 3)', '0', 'UKT: Rp 3.000.000; SKS: 6 x Rp 700.000', '0', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Industri S2 (Semester 4)', '1', 'UKT: Rp 3.000.000; SKS: 6 x Rp 700.000', '0', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Teknik Kimia
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Kimia', '0', 'UKT: Rp 2.500.000; SKS: 18 x Rp 300.000; Praktikum: Rp 840.000; DPP: Rp 12.500.000', '21240000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Kimia', '1', 'UKT: Rp 2.500.000; SKS: 18 x Rp 300.000; Praktikum: Rp 840.000', '8740000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Kimia (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; Jalur Rekognisi Pembelajaran Lampau (RPL) jenjang S1', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Teknik Lingkungan
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Lingkungan', '0', 'UKT: Rp 2.500.000; SKS: 20 x Rp 350.000; Praktikum: Rp 1.430.000; DPP: Rp 15.000.000', '25930000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Lingkungan', '1', 'UKT: Rp 2.500.000; SKS: 20 x Rp 350.000; Praktikum: Rp 1.345.000', '10845000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Teknik Mesin
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Mesin', '0', 'UKT: Rp 2.500.000; SKS: 20 x Rp 350.000; DPP: Rp 15.000.000', '24500000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Mesin', '1', 'UKT: Rp 2.500.000; SKS: 19 x Rp 350.000', '9150000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Mesin (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; Jalur Rekognisi Pembelajaran Lampau (RPL) jenjang S1', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Mesin S2 (Semester 1)', '0', 'UKT: Rp 3.000.000; SKS: 12 x Rp 750.000', '12000000', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Mesin S2 (Semester 2)', '1', 'UKT: Rp 3.000.000; SKS: 12 x Rp 750.000', '12000000', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Mesin S2 (Semester 3)', '0', 'UKT: Rp 3.000.000; SKS: 6 x Rp 750.000', '7500000', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Mesin S2 (Semester 4)', '1', 'UKT: Rp 3.000.000; SKS: 6 x Rp 750.000', '7500000', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Mesin S2 (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 250.000; Jalur Rekognisi Pembelajaran Lampau (RPL) jenjang S2', '9500000', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Biaya: Teknik Sipil
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Sipil', '0', 'UKT: Rp 2.500.000; SKS: 20 x Rp 350.000; Praktikum: Rp 310.000; DPP: Rp 17.500.000', '27310000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Sipil', '1', 'UKT: Rp 2.500.000; SKS: 20 x Rp 350.000; Praktikum: Rp 265.000', '9765000', NULL, '0', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Sipil (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 100.000; Jalur Rekognisi Pembelajaran Lampau (RPL) jenjang S1', '8500000', NULL, '2', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Sipil S2 (Semester 1)', '0', 'UKT: Rp 3.000.000; SKS: 12 x Rp 850.000', '13200000', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Sipil S2 (Semester 2)', '1', 'UKT: Rp 3.000.000; SKS: 12 x Rp 850.000', '13200000', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Sipil S2 (Semester 3)', '0', 'UKT: Rp 3.000.000; SKS: 6 x Rp 850.000', '8100000', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Sipil S2 (Semester 4)', '1', 'UKT: Rp 3.000.000; SKS: 6 x Rp 850.000', '8100000', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `biaya_pendidikan` (`nama`, `semester`, `note`, `biaya`, `url`, `jenis`, `tenggat_bayar`, `created_at`, `updated_at`) VALUES
  ('Teknik Sipil S2 (RPL)', '0', 'Pendaftaran: Rp 500.000; Konversi/SKS: Rp 250.000; Jalur Rekognisi Pembelajaran Lampau (RPL) jenjang S2', '9500000', NULL, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');


-- ============================================
-- JALUR SELEKSI (dari data/structured/jalur/)
-- ============================================

-- [1] Jalur: MAGISTER
INSERT INTO `jalur_seleksi` (`id`, `nama`, `banner`, `slug`, `deskripsi`, `biaya_daftar`, `is_active`, `periode_id`, `created_at`, `updated_at`) VALUES
  (1, 'MAGISTER', NULL, 'magister', 'Penerimaan Program Magister (S2) Itenas terbuka bagi lulusan sarjana (S1) yang ingin melanjutkan pendidikan ke jenjang pascasarjana. Itenas menawarkan program Magister Teknik Sipil, Magister Teknik Mesin, dan Magister Teknik Industri dengan kurikulum yang dirancang untuk menjawab tantangan industri dan kebutuhan pengembangan keilmuan secara profesional.', 250000, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Persyaratan Jalur ID=1
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (1, 'Peserta seleksi harus sudah lulus sarjana dari program studi yang terakreditasi atau yang disamakan.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (1, 'Calon mahasiswa wajib melengkapi persyaratan administrasi dengan mengisi biodata dan menyerahkan foto secara online, selain itu juga menyerahkan surat pernyataan, salinan akte kelahiran/surat kenal lahir, salinan ijazah S1 yang dilegalisir, transkrip akademik yang dilegalisir serta sertifikat nilai English Language Proficiency Test (ELPT Itenas) atau TOEFL ITP.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (1, 'Calon mahasiswa juga harus mempunyai kesehatan yang memadai sehingga kelancaran proses pembelajaran di program studinya tidak akan terganggu.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Cara Pendaftaran Jalur ID=1
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (1, 'Calon peserta magister melakukan pengisian data awal berupa nama, tempat tanggal lahir, dan jumlah pilihan Program Studi melalui laman khusus SPMB untuk mendapatkan Nomor Virtual Account (VA).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (1, 'Calon peserta magister melakukan pembayaran di bank atau ATM melalui proses transfer dengan rekening tujuan adalah Nomor VA.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (1, 'Peserta seleksi magister melakukan pendaftaran di laman khusus SPMB dengan melengkapi formulir yang tersedia serta mengunggah pas foto terbaru berwarna & ukuran file maks. 100 kb. Dan cetak kartu ujian', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (1, 'Menyerahkan persyaratan ke Biro Akademik', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (1, 'Mengikuti wawancara sesuai Prodi yang dipilih berdasarkan jadwal yang ditetapkan oleh masing-masing program.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Dokumen Pendaftaran Jalur ID=1
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (1, 'Surat pernyataan dapat diunduh di disini: https://drive.google.com/file/d/1ZHXQsFUz5QReJJR-2qZTgM3yja15j-vu/view?usp=sharing', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (1, 'Salinan Akte Kelahiran/Surat Kenal Lahir', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (1, 'Salinan Ijazah S1 yang dilegalisir', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (1, 'Transkrip akademik yang dilegalisir', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (1, 'Sertifikat nilai English Language Proficiency Test (ELP ITENAS atau TOEFL ITP)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- [2] Jalur: ODT
INSERT INTO `jalur_seleksi` (`id`, `nama`, `banner`, `slug`, `deskripsi`, `biaya_daftar`, `is_active`, `periode_id`, `created_at`, `updated_at`) VALUES
  (2, 'ODT', NULL, 'odt', 'One Day Test (ODT) adalah jalur seleksi mahasiswa baru Itenas yang dilaksanakan secara daring. Peserta ODT dapat memilih sendiri tanggal ujian sesuai jam kerja yang tersedia. Pilihan jam ujian terdiri dari dua sesi: Sesi 1 pukul 08.00 WIB dan Sesi 2 pukul 13.00 WIB. Ujian berlangsung selama satu hari, dan hasilnya diumumkan satu hari setelah tes selesai. Jalur ini menawarkan proses seleksi yang cepat, fleksibel, dan praktis.', 350000, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Persyaratan Jalur ID=2
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (2, 'Memiliki ijazah (Surat Tanda Tamat Belajar) tingkat Sekolah Menengah Atas atau Sekolah Menengah Kejuruan.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (2, 'Bagi peserta seleksi baru berkewarganegaraan asing, harus memenuhi seluruh persyaratan ijin belajar yang dikeluarkan Kelembagaan Ilmu Pengetahuan, Teknologi, dan Pendidikan Tinggi, Kementerian Riset, Teknologi, dan Pendidikan Tinggi.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (2, 'Memenuhi persyaratan administrasi tentang prosedur pendaftaran.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (2, 'Bebas buta warna total maupun parsial untuk yang memilih Program Studi Teknik Lingkungan, Teknik Kimia, Desain Interior, Desain Produk, dan Desain Komunikasi Visual.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (2, 'Mengikuti proses pendaftaran sesuai dengan tata cara pendaftaran SPMB jalur One Day Test pada jadwal yang telah ditetapkan.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (2, 'Mengikuti ujian sesuai Program Studi yang dipilih pada jadwal yang telah ditetapkan.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (2, 'Memiliki nilai ujian saringan masuk yang lebih tinggi dari batas nilai yang dapat diterima sebagai mahasiswa.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (2, 'Berkelakuan baik yang ditunjukan dengan Surat Keterangan Berkelakuan Baik yang dikeluarkan oleh sekolah asal atau kepolisian Negara Republik Indonesia.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (2, '*Pengumuman hasil ODT akan keluar 1 hari setelah test', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Cara Pendaftaran Jalur ID=2
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (2, 'Calon peserta One Day Test melakukan pengisian data awal berupa nama, tempat tanggal lahir, dan jumlah pilihan Program Studi melalui laman khusus SPMB.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (2, 'Calon peserta ODT mendapatkan nomor Virtual Account (VA) untuk melakukan pembayaran di bank atau ATM melalui proses transfer dengan rekening tujuan adalah Nomor VA.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (2, 'Peserta seleksi ODT melakukan pendaftaran di laman khusus SPMB dengan melengkapi formulir yang tersedia serta mengunggah pas foto terbaru.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (2, 'Calon peserta melakukan finalisasi dan mencetak Kartu Peserta Test', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (2, 'Ujian One Day Test dilaksanakan secara online link odt.itenas.ac.id', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- [3] Jalur: PMDK
INSERT INTO `jalur_seleksi` (`id`, `nama`, `banner`, `slug`, `deskripsi`, `biaya_daftar`, `is_active`, `periode_id`, `created_at`, `updated_at`) VALUES
  (3, 'PMDK', NULL, 'pmdk', 'Jalur PMDK Itenas adalah jalur masuk tanpa tes yang ditujukan bagi siswa berprestasi, aktif berorganisasi, atau memiliki nilai akademik yang baik. Tersedia tiga jalur: Jalur Prestasi (non-akademik), Jalur Keorganisasian, dan Jalur Akademik.', 50000, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Persyaratan Jalur ID=3
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (3, 'Diperuntukkan bagi siswa Kelas 12 atau yang belum lulus SMA/SMK/MA sederajat.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (3, 'Bagi Warga Negara Asing (WNA), wajib memenuhi seluruh persyaratan izin belajar dari kementerian terkait.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (3, 'Bebas buta warna total maupun parsial (khusus pendaftar Program Studi Teknik Lingkungan, Teknik Kimia, Desain Interior, Desain Produk, dan Desain Komunikasi Visual).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (3, 'Jalur Keorganisasian: Aktif dalam organisasi di sekolah atau luar sekolah (misalnya Pengurus OSIS, Unit Kegiatan Siswa).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (3, 'Jalur Prestasi (Non-Akademik): Memiliki penghargaan minimal juara 3 tingkat provinsi/nasional atau finalis tingkat internasional dalam 2 tahun terakhir.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (3, 'Jalur Prestasi Media Sosial: Aktif sebagai Content Creator. Syarat minimum: Youtube (1.000 subscribers) atau Instagram/TikTok (10.000 followers). Konten wajib bebas SARA, pornografi, dan ujaran kebencian.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (3, 'Jalur Akademik: Merupakan lulusan tahun 2026, dan memiliki nilai di atas Kriteria Ketuntasan Minimal (KKM) untuk semua mata pelajaran dari semester 1 hingga semester 4.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (3, 'Peserta seleksi Program PMDK hanya diperbolehkan mengikuti proses seleksi sebanyak satu kali.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Cara Pendaftaran Jalur ID=3
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (3, 'Calon peserta mengakses laman khusus PMDK dan mengisi data awal (nama, tempat tanggal lahir, dan 1 pilihan Program Studi) untuk mendapatkan nomor Virtual Account (VA).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (3, 'Calon peserta melakukan pembayaran biaya pendaftaran sebesar Rp 50.000 melalui transfer bank/ATM ke rekening tujuan nomor VA tersebut.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (3, 'Peserta login kembali ke laman SPMB Itenas untuk mengisi formulir pendaftaran, melengkapi biodata diri, dan mengunggah pas foto terbaru.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (3, 'Peserta mengunggah seluruh dokumen persyaratan yang diminta.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (3, 'Peserta melakukan tahap finalisasi pendaftaran dan mencetak Kartu Peserta.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Dokumen Pendaftaran Jalur ID=3
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (3, 'Pas foto asli (hasil jepretan kamera langsung, bukan foto dari pas foto yang dicetak).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (3, 'Akte Kelahiran dan Kartu Keluarga (KK).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (3, 'Kartu Tanda Penduduk (KTP) jika sudah memiliki.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (3, 'Nilai rapor kelas X dan XI (mencakup halaman identitas siswa dan nilai Semester 1 hingga 4) yang telah dilegalisir oleh Kepala Sekolah.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (3, 'Surat rekomendasi dari Kepala Sekolah untuk mengikuti seleksi jalur PMDK.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (3, 'Salinan bukti sertifikat prestasi yang dilegalisir sekolah (khusus pendaftar jalur prestasi/non-akademik).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (3, 'File PDF berisi tangkapan layar (screenshot) akun media sosial beserta tautannya (khusus pendaftar jalur prestasi media sosial).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- [4] Jalur: RPL
INSERT INTO `jalur_seleksi` (`id`, `nama`, `banner`, `slug`, `deskripsi`, `biaya_daftar`, `is_active`, `periode_id`, `created_at`, `updated_at`) VALUES
  (4, 'RPL', NULL, 'rpl', 'Program ini ditujukan bagi para pekerja, ASN, TNI/POLRI, pegawai, Praktisi, lulusan SMA/SMK dan Diploma (D3/D4) yang pernah/sedang bekerja. Program RPL dirancang untuk mempercepat waktu studi dengan pengakuan sks berdasarkan pengalaman kerja/kompetensi di masa lampau, serta memiliki waktu kuliah yang fleksibel.', 500000, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Persyaratan Jalur ID=4
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (4, 'Jenis RPL di Itenas terdiri atas dua tipe: Alih Kredit (Pengakuan hasil belajar formal yang sudah ditempuh sebelumnya) dan Perolehan Kredit (Pengakuan hasil belajar dari belajar nonformal, informal, dan/atau pengalaman kerja).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (4, 'Persyaratan Khusus RPL Tipe A Alih Kredit dan Tipe A Perolehan Kredit diatur secara spesifik dalam Pedoman yang ditetapkan Rektor.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (4, 'Persyaratan Umum khusus RPL Tipe A Perolehan Kredit: Calon peserta diwajibkan mempunyai pengalaman kerja paling sedikit 2 (dua) tahun.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (4, 'Peserta yang telah dinyatakan lolos asesmen akan mendapatkan Keputusan Rektor tentang Pengakuan Alih Kredit yang isinya mencakup: masa studi, mata kuliah yang diakui, mata kuliah yang harus ditempuh, serta jumlah SKS.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Cara Pendaftaran Jalur ID=4
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (4, 'Calon peserta melakukan pendaftaran melalui laman khusus SPMB Itenas dengan mengisi data awal (nama, tempat tanggal lahir, jumlah pilihan Program Studi) untuk mendapatkan Nomor Virtual Account (VA).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (4, 'Calon peserta melakukan pembayaran biaya pendaftaran sebesar Rp 500.000 di bank atau ATM melalui proses transfer ke rekening tujuan Nomor VA.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (4, 'Calon peserta melakukan verifikasi pembayaran untuk mendapatkan nomor peserta dan kode PIN.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (4, 'Calon peserta login dan melengkapi pengisian biodata pada laman https://rpl.itenas.ac.id/.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (4, 'Calon peserta mengunggah dokumen persyaratan secara lengkap.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (4, 'Bagi peserta yang telah memenuhi persyaratan, wajib mengikuti tahapan asesmen dan rekognisi yang dilakukan oleh Tim Asesor RPL Itenas.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Dokumen Pendaftaran Jalur ID=4
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (4, 'Ijazah dari jenjang pendidikan sebelumnya.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (4, 'Transkrip Nilai dari jenjang pendidikan sebelumnya.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (4, 'Sertifikat Akreditasi Program Studi dan Perguruan Tinggi asal pada saat lulus (Khusus pendaftar RPL Tipe A Alih Kredit).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (4, 'Surat pernyataan dari peserta (Khusus pendaftar RPL Tipe A Perolehan Kredit).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (4, 'Daftar riwayat hidup (Khusus pendaftar RPL Tipe A Perolehan Kredit).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (4, 'Surat keterangan berkelakuan baik dari kepolisian (Khusus pendaftar RPL Tipe A Perolehan Kredit).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (4, 'Dokumen asesmen mandiri terhadap Capaian Pembelajaran / CP (Khusus pendaftar RPL Tipe A Perolehan Kredit).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (4, 'Dokumen pendukung lainnya terkait pengalaman kerja (Khusus pendaftar RPL Tipe A Perolehan Kredit).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- [5] Jalur: SNBT
INSERT INTO `jalur_seleksi` (`id`, `nama`, `banner`, `slug`, `deskripsi`, `biaya_daftar`, `is_active`, `periode_id`, `created_at`, `updated_at`) VALUES
  (5, 'SNBT', NULL, 'snbt', 'Institut Teknologi Nasional memberikan kesempatan kepada lulusan SMA dan SMK untuk bisa mengikuti seleksi masuk melalui jalur UTBK SNBT (Seleksi Bersama Berdasarkan Test) Tahun 2025 atau 2026. Sertifikat yang dapat digunakan adalah Sertifikat UTBK/SNBT 2025 dan 2026.', 50000, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Persyaratan Jalur ID=5
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (5, 'Sertifikat hasil UTBK/SNBT 2025 atau 2026', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (5, 'Pas foto terbaru 3x4.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (5, 'Akte Kelahiran', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (5, 'Kartu Tanda Penduduk (KTP)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (5, 'Kartu Keluarga (KK)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (5, '*Pengumuman hasil UTBK/SNBT diproses setelah calon mahasiswa baru melakukan finalisasi (paling lambat 2 hari kerja)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Cara Pendaftaran Jalur ID=5
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (5, 'Proses pendaftaran dilakukan secara online melalui laman SPMB Itenas.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (5, 'Calon peserta jalur UTBK melakukan pengisisan data awal berupa nama, tempat tanggal lahir dan 2 Program Studi yang dipilih untuk mendapatkan nomor Virtual Account (VA).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (5, 'Calon peserta melakukan pembayaran di Bank atau ATM melalui proses transfer dengan rekening tujuan adalah nomor VA.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (5, 'Peserta seleksi mengisi formulir pendaftaran jalur UTBK, data diri, dan mengunggah pas foto terbaru melalui laman SPMB Itenas.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (5, 'Peserta seleksi mengunggah dokumen persyaratan:', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- [6] Jalur: TKA
INSERT INTO `jalur_seleksi` (`id`, `nama`, `banner`, `slug`, `deskripsi`, `biaya_daftar`, `is_active`, `periode_id`, `created_at`, `updated_at`) VALUES
  (6, 'TKA', NULL, 'tka', 'Tes Kemampuan Akademik (TKA) adalah jalur seleksi penerimaan mahasiswa baru untuk menilai kemampuan akademik calon mahasiswa secara objektif dan terstandar, terbuka bagi semua program studi, dengan pendaftaran yang dilakukan secara online melalui laman SPMB Itenas.', 50000, '1', NULL, '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Persyaratan Jalur ID=6
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (6, 'SPMB jalur TKA dibuka untuk semua Program Studi.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (6, 'Peserta seleksi yang dapat diterima melalui jalur TKA harus memenuhi syarat sebagai berikut:', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (6, 'Memenuhi persyaratan administratif sebagai peserta seleksi, sebagaimana tercantum pasal 3 (tiga);', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (6, 'Memiliki nilai TKA', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (6, 'Mata uji TKA untuk SMA/MA/program paket C/ sederajat dan SMK/MAK terdiri atas: Bahasa Indonesia, Matematika, Bahasa Inggris, dan mata pelajaran pilihan.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `persyaratan_umum` (`jalur_id`, `persyaratan`, `created_at`, `updated_at`) VALUES
  (6, '*Peserta seleksi dinyatakan lulus apabila nilai sekurang-kurangnya 50 (lima puluh) pada setiap mata uji dan kategori capaian pada setiap mata uji TKA sekurang-kurangnya Memadai.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Cara Pendaftaran Jalur ID=6
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (6, 'Pendaftaran dilakukan secara online melalui laman SPMB Itenas, calon peserta TKA melakukan pengisian data awal berupa pilihan jalur TKA, nama, tempat tanggal lahir, jenis kelamin, email dan nomor handphone untuk mendapatkan nomor Virtual Account (VA).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (6, 'Calon peserta TKA melakukan pembayaran di Bank atau ATM melalui proses transfer dengan rekening tujuan adalah nomor VA.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (6, 'Calon peserta TKA melakukan verifikasi pembayaran dan akan menerima Nomor Peserta serta kode PIN yang akan dikirim melalui email dan SMS.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (6, 'Peserta seleksi melakukan pendaftaran di laman khusus SPMB dengan melengkapi isian biodata dan melampirkan data (upload)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `cara_pendaftaran` (`jalur_id`, `deskripsi`, `created_at`, `updated_at`) VALUES
  (6, 'Peserta melakukan finalisasi dan mencetak Kartu Peserta.', '2026-05-30 19:41:41', '2026-05-30 19:41:41');

-- Dokumen Pendaftaran Jalur ID=6
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (6, 'Pas foto terbaru', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (6, 'Akte kelahiran', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (6, 'Kartu Tanda Penduduk (KTP)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (6, 'Kartu Keluarga (KK)', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (6, 'Surat keterangan tidak buta warna total maupun parsial dari dokter (6 bulan terakhir), 1 (satu) rangkap fotocopy dan memperlihatkan yang asli bagi yang akan pindah ke Program Studi Teknik Kimia, Teknik Lingkungan, Desain Interior, Desain Produk, dan Desain Komunikasi Visual', '2026-05-30 19:41:41', '2026-05-30 19:41:41');
INSERT INTO `dokumen_pendaftaran` (`jalur_id`, `dokumen`, `created_at`, `updated_at`) VALUES
  (6, 'Surat Pernyataan Dana Pengembangan Pendidikan (DPP).', '2026-05-30 19:41:41', '2026-05-30 19:41:41');


SET FOREIGN_KEY_CHECKS = 1;
