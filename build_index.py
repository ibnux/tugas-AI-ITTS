# build_index.py - Membangun Index dari PDF
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    Settings
)
from llama_index.readers.file import PyMuPDFReader 
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

# Gunakan HuggingFace embedding dengan model tertentu
embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)
Settings.embed_model = embed_model
print("Using HuggingFace embedding: BAAI/bge-small-en-v1.5")

DATA_DIR = "./data"
PERSIST_DIR = "./storage"

def build_and_persist_index():
    print(f"📁 Memindai {DATA_DIR}...")
    
    # Cek file PDF
    pdf_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.pdf')]
    print(f"Ditemukan {len(pdf_files)} file PDF: {pdf_files}")
    
    if not pdf_files:
        print("Tidak ada file PDF! Letakkan file .pdf di ./data/")
        return
    
    # SimpleDirectoryReader + PyMuPDFReader
    documents = SimpleDirectoryReader(
        input_dir=DATA_DIR,
        required_exts=[".pdf"],
        # Gunakan instance PyMuPDFReader, bukan class
        file_extractor={".pdf": PyMuPDFReader()}
    ).load_data()
    
    print(f"\n📄 Memuat {len(documents)} dokumen:")
    total_chars = 0
    for i, doc in enumerate(documents):
        chars = len(doc.text.strip())
        total_chars += chars
        file_name = doc.metadata.get('file_name', 'Unknown')
        print(f"  - {file_name}: {chars:,} chars")
        if chars > 0:
            print(f"    Preview: {doc.text.strip()[:100]}...")
    
    print(f"\nTotal teks: {total_chars:,} karakter")
    
    if total_chars == 0:
        print("Tidak ada teks yang diambil! Coba PDF lain atau install pikepdf")
        return
    
    # Bangun index vector
    print("\nMembangun vector index...")
    index = VectorStoreIndex.from_documents(documents)
    
    # Simpan index
    storage_context = index.storage_context
    storage_context.persist(persist_dir=PERSIST_DIR)
    
    print("\n BERHASIL! Index tersimpan.")
    print("Jalankan: streamlit run app.py")

if __name__ == "__main__":
    build_and_persist_index()
