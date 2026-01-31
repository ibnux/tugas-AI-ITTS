# 🤖 Setup Ollama + PDF Chat

## Alur Cara Kerja

```
PDF Files → PyMuPDFReader → LlamaIndex → Vector Index → Stored
                                                            ↓
User Question → Vector Search (Retrieve) → Ollama LLM (Generate) → Natural Answer
```

## Step-by-Step Setup

### 1️⃣ Install Ollama

**Option A: Mac dengan Homebrew**
```bash
brew install ollama
```

**Option B: Download Manual**
Visit https://ollama.ai dan download untuk Mac/Linux/Windows

### 3️⃣ Pull Model (Di Terminal Baru)

```bash

# Recommended:  llama3.2:1b untuk macbook pro M2
ollama pull  llama3.2:1b

# Atau alternative:
ollama pull mistral        #  Mistral (cepat dan berkualitas)
ollama pull neural-chat    # Lebih kecil, lebih cepat
ollama pull llama2         # Lebih besar, lebih accurate
```

Tunggu sampai selesai (bisa 5-15 menit tergantung koneksi).

### 2️⃣ Jalankan Ollama Server

```bash
ollama serve
```

Output akan seperti:
```
pulling manifest
pulling 1d7ad209...
...
success
```

**JANGAN CLOSE TERMINAL INI!** Biarkan Ollama terus berjalan.


### 4️⃣ Verify Setup

```bash
# Test Ollama berhasil
curl http://localhost:11434/api/tags

# Output akan menunjukkan model yang sudah ter-install
```

### 5️⃣ Build Index dari PDF (Jika belum)

```bash
python build_index.py
```

Output:
```
✅ SUCCESS! Index saved to ./storage/
```

### 6️⃣ Jalankan Chat App

```bash
streamlit run app.py
```

Browser otomatis terbuka

---

## 🚀 Cara Pakai

1. **Ketik pertanyaan** di chat input
2. **Ollama akan:**
   - Retrieve dokumen relevan dari index
   - Membaca isi dokumen
   - Generate jawaban natural
3. **Dapatkan jawaban** dalam format conversational

### Contoh:

**User:** "Bagaimana prosedur wisuda di ITTS?"

**Ollama:** 
```
Berdasarkan dokumen akademik ITTS, prosedur wisuda melibatkan beberapa tahap:

1. Pertama, mahasiswa harus memastikan semua tunggakan akademik dan keuangan 
sudah lunas.

2. Kemudian, mendaftar ke bagian akademik dengan melengkapi semua dokumen 
yang diperlukan.

3. Setelah itu, mengikuti acara wisuda sesuai jadwal yang sudah ditentukan.

4. Terakhir, pengambilan ijazah dan transkrip nilai di bagian akademik.

Sumber: Buku_Pedoman_Akademik_2025_2026.pdf
```

---

## 🔧 Troubleshooting

### ❌ "Connection refused"
```
Pastikan Ollama server running:
ollama serve

(Di terminal yang berbeda)
```

### ❌ "Model not found"
```
Pull model lagi:
ollama pull mistral
```

### ❌ Jawaban lambat
```
Model Mistral mungkin sudah cukup cepat.
Jika masih lambat, coba yang lebih kecil:
ollama pull neural-chat
```

Lalu update di app.py:
```python
OLLAMA_MODEL = "neural-chat"
```

---

## 📊 Model Comparison

| Model | Size | Speed | Quality | RAM |
|-------|------|-------|---------|-----|
| neural-chat | 4 GB | Fast ⚡ | Good | 8 GB |
| mistral | 5 GB | Fast | Great | 12 GB |
| llama2 | 7 GB | Medium | Excellent | 16 GB |

---

## 💡 Tips

**Best Practice:**
- Keep Ollama running in background
- Use specific questions for better answers
- Chat history tersimpan per session

**Performance:**
- First response lebih lambat (model loading)
- Subsequent responses lebih cepat
- Jawaban bisa 5-30 detik tergantung model

---

## 🎉 Setup Complete!

Semuanya sudah siap:
- ✅ PDF indexed
- ✅ App configured  
- ✅ Ollama integrated

**Mulai chat:** `streamlit run app.py`
