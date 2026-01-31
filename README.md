# Mata Kuliah	:	Artificial Intelligence

Kode Mata Kuliah	:	SI148.   
Semester	:	3.   
SKS	:	3.   
Dosen Pengampu	:	Dhika Rizki Anbiya, S.Kom, M.T.    
Tanggal Ujian	:	28 Januari 2026.    
Waktu Ujian	:	19.00 – 20.00 WIB.   

## TIM

- Ibnu Maksum

## Penjelasan Aplikasi

Project ini dibuat menggunakan Macbook Pro M2, memanfaatkan prosesor Apple Silicon.

app.py - Aplikasi Chat PDF dengan Ollama LLM Lokal     
     
Aplikasi ini menggunakan RAG (Retrieval-Augmented Generation) untuk:
1. Membaca dokumen PDF dari vector store (./storage/)
2. Mencari dokumen yang relevan dengan pertanyaan pengguna
3. Mengirim dokumen + pertanyaan ke Ollama
4. Ollama menghasilkan jawaban natural language
5. Menampilkan jawaban dengan sumber dokumen di Streamlit UI

## 2️⃣ Langkah Menggunakan

### Step 1: Build Index
```bash
conda create -n rag_m2 python=3.11 -y 
conda activate rag_m2
pip install -r requirements.txt

python build_index.py
```

Output:
```
✅ SUCCESS! Index saved.
💾 Stored in: ./storage/
```

### Step 2: Run App
```bash
streamlit run app.py
```

Visit: `http://localhost:8501`

### Step 3: Search!
Ketik pertanyaan apapun tentang PDF:
- "Apa itu pedoman akademik?"
- "Syarat skripsi?"
- "Bagaimana wisuda?"

## 📊 File Results

- **build_index.py**: ✅ Working
  - Membaca 5 PDF dari `./data/`
  - Mengekstrak 511,110 karakter
  - Membuat vector index dengan HuggingFace embeddings
  - Simpan ke `./storage/`

- **app.py**: ✅ Working
  - Streamlit UI untuk searching
  - Menggunakan VectorIndexRetriever
  - Tampilkan top-5 hasil relevan
  - Tanpa LLM (retrieval-only mode)

- **storage/**: ✅ Vector Store Ready
  - `default__vector_store.json`: Vector embeddings
  - `docstore.json`: Document chunks
  - `index_store.json`: Index metadata

## Fixes Applied

```python
# Before (Error)
file_extractor={".pdf": PyMuPDFReader}

# After (Fixed)
file_extractor={".pdf": PyMuPDFReader()}
```

```bash
# Before (Missing PyMuPDF)
ModuleNotFoundError: No module named 'fitz'

# After (Installed)
pip install PyMuPDF
```

```bash
# Before (torchvision conflict)
RuntimeError: operator torchvision::nms does not exist

# After (Uninstalled)
pip uninstall -y torchvision
```

## Test Retrieval

```bash
python -c "
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.retrievers import VectorIndexRetriever

embed_model = HuggingFaceEmbedding(model_name='BAAI/bge-small-en-v1.5')
Settings.embed_model = embed_model

storage_context = StorageContext.from_defaults(persist_dir='./storage')
index = load_index_from_storage(storage_context)
retriever = VectorIndexRetriever(index=index, similarity_top_k=3)

nodes = retriever.retrieve('Apa itu pedoman akademik')
for node in nodes:
    print(f'Score: {node.score:.3f} - {node.node.metadata.get(\"file_name\")}')
"
```

## Selesai!

Semuanya sudah siap. Tinggal jalankan:
```bash
python build_index.py && streamlit run app.py
```
