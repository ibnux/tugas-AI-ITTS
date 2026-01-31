# Setup Ollama + Chat PDF

## Alur Cara Kerja

```
File PDF → PyMuPDFReader → LlamaIndex → Vector Index → Disimpan
                                                            ↓
Pertanyaan User → Vector Search (Retrieve) → Ollama LLM (Generate) → Jawaban Natural
```

## Setup Step-by-Step

### Install Ollama

**Opsi A: Mac dengan Homebrew (Recommended)**
```bash
brew install ollama
```

**Opsi B: Download Manual**
Kunjungi https://ollama.ai dan download untuk Mac/Linux/Windows

### Download Model AI (Di Terminal Baru)

```bash
# Recommended: llama3.2:1b untuk MacBook Pro M2 (paling cepat)
ollama pull llama3.2:1b

# Atau pilih alternatif lain:
ollama pull mistral        # Mistral (cepat dan berkualitas tinggi)
ollama pull neural-chat    # Lebih kecil dan cepat
ollama pull llama2         # Lebih besar, lebih akurat
```

Tunggu sampai selesai (bisa 5-15 menit tergantung kecepatan internet)

### 3Jalankan Ollama Server

```bash
ollama serve
```

Output akan terlihat seperti:
```
pulling manifest
pulling 1d7ad209...
...
success
```

**PENTING: JANGAN TUTUP TERMINAL INI!** Biarkan Ollama terus berjalan di background

### Verifikasi Setup Ollama

```bash
# Test apakah Ollama berhasil terhubung
curl http://localhost:11434/api/tags

# Output akan menunjukkan model yang sudah ter-install
```

### Build Index dari PDF (Jika Belum Ada)

Di terminal baru (bukan tempat ollama serve):
```bash
python build_index.py
```

Output yang diharapkan:
```
BERHASIL! Index disimpan ke ./storage/
```

### Jalankan Chat App

```bash
streamlit run app.py
```

Browser akan otomatis terbuka di http://localhost:8501

---

## Cara Menggunakan Chat

1. **Ketik pertanyaan** di kolom input chat
2. **Ollama akan melakukan:**
   - Mencari dokumen relevan dari vector index
   - Membaca isi dokumen yang ditemukan
   - Generate jawaban yang natural dan conversational
3. **Dapatkan jawaban** dengan format seperti percakapan biasa

### Contoh Penggunaan:

**User:** "Bagaimana prosedur wisuda di ITTS?"

**Ollama:** 
```
Berdasarkan dokumen akademik ITTS, prosedur wisuda melibatkan beberapa tahap:

1. Pertama, mahasiswa harus memastikan semua tunggakan akademik dan 
   keuangan sudah lunas.

2. Kemudian, mendaftar ke bagian akademik dengan melengkapi semua 
   dokumen yang diperlukan.

3. Setelah itu, mengikuti acara wisuda sesuai jadwal yang sudah ditentukan.

4. Terakhir, pengambilan ijazah dan transkrip nilai di bagian akademik.

Sumber: Buku_Pedoman_Akademik_2025_2026.pdf
```

---

## Troubleshooting (Pemecahan Masalah)

### Error: "Connection refused"
```
SOLUSI: Pastikan Ollama server sudah running:

Terminal 1:
$ ollama serve

Terminal 2 (baru):
$ streamlit run app.py
```

### Error: "Model not found"
```
SOLUSI: Download model terlebih dahulu:
$ ollama pull llama3.2:1b
```

### Jawaban terlalu lambat (timeout)
```
SOLUSI: Gunakan model yang lebih ringan:
$ ollama pull neural-chat

Kemudian update OLLAMA_MODEL di app.py:
OLLAMA_MODEL = "neural-chat"
```

---

## Perbandingan Model

| Model | Ukuran | Kecepatan | Kualitas | RAM Min |
|-------|--------|-----------|----------|----------|
| neural-chat | 4 GB | Sangat Cepat | Baik | 8 GB |
| llama3.2:1b | 2 GB | Paling Cepat | Baik | 6 GB |
| mistral | 5 GB | Cepat | Sangat Baik | 12 GB |
| llama2 | 7 GB | Sedang | Excellent | 16 GB |

**Rekomendasi:** Untuk MacBook M2, gunakan `llama3.2:1b` atau `neural-chat`

---

## Tips & Best Practice

### Praktik Terbaik:
- Biarkan Ollama berjalan di background (jangan tutup terminal)
- Gunakan pertanyaan yang spesifik dan detail untuk hasil lebih baik
- Chat history tersimpan per session (tidak persistent)
- Jangan refresh halaman jika ingin mempertahankan riwayat chat

### Performa:
- Response pertama lebih lambat (model loading ke memory)
- Response berikutnya lebih cepat
- Lama jawaban: 5-30 detik tergantung model dan panjang dokumen
- MacBook M2 bisa mencapai timeout jika konteks terlalu panjang

### Optimisasi MacBook M2:
- Gunakan `similarity_top_k=2` (hanya 2 dokumen)
- Set `response_mode="compact"` (jawaban lebih ringkas)
- Jangan buka aplikasi berat lain (browser banyak tab, Xcode, dll)

---

## Setup Selesai!

Semuanya sudah siap digunakan:
- PDF sudah diindex
- App sudah dikonfigurasi
- Ollama sudah terintegrasi

### Mulai Menggunakan:
```bash
streamlit run app.py
```

Buka http://localhost:8501 di browser dan mulai bertanya!
