# Aplikasi Streamlit — Simulasi Limit (Contoh Kasus 2.1.1)

**Materi:** Bab 2, Subbab 2.1, Contoh Kasus 1 — Menghitung Kecepatan Sesaat Sebuah Kendaraan.

**Model:** posisi s(t)=t² meter dengan waktu t≥0 detik; ingin menentukan kecepatan sesaat pada t=3 detik.

## Cara menggunakan pada laptop Windows

1. Pastikan Python 3.10 atau lebih baru terpasang.
2. Buka Terminal / PowerShell pada folder yang berisi `streamlit_app.py` dan `requirements.txt`.
3. Jalankan:

   ```powershell
   python -m pip install -r requirements.txt
   python -m streamlit run streamlit_app.py
   ```

4. Browser akan terbuka, biasanya di http://localhost:8501.
5. Gunakan tombol **Putar animasi**, **Jeda**, **Ulangi**, dan **Perbesar grafik**.

## Deploy gratis melalui Streamlit Community Cloud

1. Buat repo GitHub dan unggah `streamlit_app.py` serta `requirements.txt` di root repo.
2. Di https://share.streamlit.io, pilih repo tersebut.
3. Set **Main file path** ke `streamlit_app.py` lalu Deploy.

## Tujuan pembelajaran

- Membedakan kecepatan rata-rata dan kecepatan sesaat.
- Memahami pendekatan dari kiri dan kanan.
- Menyadari pembagian 0/0 tidak terdefinisi, tetapi limit mungkin ada.
- Menyusun tabel perhitungan, menafsirkan grafik posisi dan secan, serta memverifikasi limit secara aljabar.

Acuan konsep: Varberg, Purcell, Rigdon, *Calculus Early Transcendentals*, Bab 2, §2.1. Model latihan dan aplikasinya disusun sebagai pendamping pembelajaran.
