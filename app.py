#!/usr/bin/env python3
"""
app.py - Aplikasi Chat PDF dengan Ollama LLM Lokal

Aplikasi ini menggunakan RAG (Retrieval-Augmented Generation) untuk:
1. Membaca dokumen PDF dari vector store (./storage/)
2. Mencari dokumen yang relevan dengan pertanyaan pengguna
3. Mengirim dokumen + pertanyaan ke Ollama
4. Ollama menghasilkan jawaban natural language
5. Menampilkan jawaban dengan sumber dokumen di Streamlit UI
"""

import streamlit as st
from llama_index.core import (
    StorageContext,          # Mengelola penyimpanan index vector
    load_index_from_storage, # Memuat index yang sudah disimpan
    Settings                 # Konfigurasi global LlamaIndex
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

# KONFIGURASI APLIKASI
PERSIST_DIR = "./storage"                    # Path tempat vector store disimpan
OLLAMA_BASE_URL = "http://localhost:11434"   # Endpoint Ollama lokal
OLLAMA_MODEL = "llama3.2:1b"                 # Model yang ringan dan cepat untuk M2


@st.cache_resource
def load_query_engine():
    """
    Fungsi untuk memuat query engine dengan Ollama LLM
    
    Tahapan:
    1. Set embedding model (HuggingFace) untuk konversi text ke vector
    2. Set Ollama LLM untuk generate jawaban
    3. Muat index yang sudah disimpan dari ./storage
    4. Buat query engine dengan konfigurasi optimal
    
    Returns:
        tuple: (query_engine, is_available) - engine untuk query atau None jika error
    """
    
    # Set model embedding (mengkonversi teks ke vektor numerik)
    embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"  # Model kecil tapi akurat
    )
    Settings.embed_model = embed_model
    
    # Set Ollama LLM untuk generate jawaban
    try:
        llm = Ollama(
            model=OLLAMA_MODEL,                      # Model: llama3.2:1b
            base_url=OLLAMA_BASE_URL,                # Hubung ke Ollama lokal
            temperature=0.5,                         # Kontrol kreativitas (0.5 = balanced)
            request_timeout=600.0,                   # Timeout 10 menit untuk M2
            additional_kwargs={"num_ctx": 4096}      # Maksimal konteks 4096 tokens
        )
        Settings.llm = llm
        
        # Load vector index dari storage
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
        
        # Buat query engine dengan optimasi untuk MacBook M2
        # similarity_top_k=2: ambil 2 dokumen paling relevan (tidak 3, untuk kurangi beban)
        # response_mode="compact": jawaban lebih ringkas dan cepat
        return index.as_query_engine(similarity_top_k=2, response_mode="compact"), True
        
    except Exception as e:
        # Error jika Ollama tidak bisa diakses
        print(f"Error loading Ollama: {e}")
        return None, False


def main():
    """
    Fungsi utama aplikasi Streamlit
    
    Menangani:
    - Konfigurasi halaman dan title
    - Inisialisasi session state untuk chat history
    - Load query engine
    - Display chat interface
    - Handle user input dan generate response
    """
    
    # Konfigurasi halaman Streamlit
    st.set_page_config(
        page_title="Pedoman Akademik ITTS - Chat PDF dengan Ollama",
        layout="wide"
    )
    
    # Header dan title aplikasi
    st.title("Asisten Chat Pedoman Akademik ITTS")
    st.markdown("Chat dengan Ollama untuk menjawab pertanyaan tentang isi Pedoman Akademik ITTS!")
    
    # Initialize chat history di session state
    # Session state memastikan chat history tetap ada saat Streamlit rerun
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Load query engine (embedding model + Ollama LLM + vector index)
    query_engine, is_available = load_query_engine()
    
    # Jika Ollama tidak tersedia, tampilkan error
    if not is_available:
        st.error("""
        **Ollama tidak tersedia!**
        
        Silakan ikuti langkah berikut:
        1. Install Ollama dari https://ollama.ai
        2. Buka terminal dan jalankan: `ollama serve`
        3. Di terminal baru, jalankan: `ollama pull llama3.2:1b`
        4. Refresh halaman ini
        """)
        return
    
    # Tampilkan pesan sukses jika Ollama terhubung
    st.success("Ollama terhubung! Chat engine siap digunakan.")
    
    # Tampilkan informasi tentang aplikasi
    st.info(f"""
    **  Konfigurasi Sistem:**
    - RAG Framework: LlamaIndex
    - LLM: Ollama {OLLAMA_MODEL}
    - Embedding: HuggingFace BAAI/bge-small-en-v1.5
    - Vector Store: {PERSIST_DIR}/
    - Ollama Endpoint: {OLLAMA_BASE_URL}
    """)
    
    # Display chat history (semua pesan yang sudah dikirim)
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])
    
    # Input box untuk user mengetik pertanyaan
    if prompt := st.chat_input("Tanya tentang isi PDF Anda..."):
        # Tambah pesan user ke chat history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "avatar": "🧑"
        })
        
        # Display pesan user di chat bubble
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)
        
        # Loading spinner sambil Ollama memproses
        with st.spinner("Ollama sedang membaca dokumen dan menyusun jawaban..."):
            try:
                # Query engine melakukan tahapan RAG:
                # 1. Embedding pertanyaan menjadi vektor
                # 2. Cari 2 dokumen paling relevan di vector store
                # 3. Ambil text dari dokumen
                # 4. Kirim pertanyaan + konteks dokumen ke Ollama
                # 5. Ollama generate jawaban natural language
                response = query_engine.query(prompt)
                
                # Konversi response object ke string
                answer = str(response)
                
                # Tambahkan informasi sumber dokumen
                if response.source_nodes:
                    answer += "\n\n---\n** Dokumen Sumber:**\n"
                    for i, node in enumerate(response.source_nodes, 1):
                        # Ambil nama file dari metadata
                        file_name = node.node.metadata.get('file_name', 'Unknown')
                        # Ambil relevance score (0.0 - 1.0)
                        score = node.score
                        answer += f"{i}. {file_name} (relevansi: {score:.0%})\n"
                
                # Tambah jawaban ke chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "avatar": "🤖"
                })
                
                # Display jawaban di chat bubble
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(answer)
                
            except Exception as e:
                # Handle error saat query
                error_msg = f"""
                Terjadi error: {str(e)}
                
                **Solusi:**
                - Pastikan Ollama sudah running: `ollama serve`
                - Cek apakah model llama3.2:1b sudah didownload: `ollama pull llama3.2:1b`
                - Tunggu beberapa saat dan coba lagi
                """
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "avatar": "🤖"
                })
                with st.chat_message("assistant", avatar="🤖"):
                    st.error(error_msg)
    
    # SIDEBAR - Informasi dan kontrol
    with st.sidebar:
        # Tampilkan informasi tentang teknologi
        st.subheader("Tentang Aplikasi")
        st.write("""
        **Tim:**
        - **Ibnu Maksum** - 1002230031
                 
        **Stack Teknologi:**
        - **LlamaIndex** - RAG Framework untuk semantic search
        - **Ollama** - Local LLM (tidak perlu API key)
        - **HuggingFace** - Embedding model untuk vector representation
        - **Streamlit** - Web UI framework
        
        **Cara Kerja:**
        1. User bertanya → konversi ke vector
        2. Cari dokumen relevan di vector store
        3. Kirim dokumen + pertanyaan ke Ollama
        4. Ollama generate jawaban berdasarkan dokumen
        5. Tampilkan jawaban + sumber dokumen
        """)
        
        # Tampilkan jumlah pesan
        st.write("")
        st.write(f"**Total Pesan:** {len(st.session_state.messages)} messages")
        
        # Tombol untuk clear chat history
        if st.button("Hapus Riwayat Chat"):
            st.session_state.messages = []
            st.rerun()
        
        st.divider()
        
        # Tampilkan konfigurasi sistem
        st.subheader("Konfigurasi Sistem")
        st.write(f"**Model LLM:** {OLLAMA_MODEL}")
        st.write(f"**Ollama URL:** {OLLAMA_BASE_URL}")
        st.write("**Embedding:** BAAI/bge-small-en-v1.5")
        st.write("**Vector Store:** ./storage/")
        
        # Tampilkan model alternatif yang bisa digunakan
        with st.expander("Model Ollama Alternatif"):
            st.code("""
# Model cepat (untuk MacBook M2):
ollama pull llama3.2:1b       # Recommended
ollama pull neural-chat       # Sangat cepat

# Model lebih akurat:
ollama pull mistral           # Balanced
ollama pull llama3.2:3b       # Lebih detail

# Model specialist:
ollama pull dolphin-mixtral   # Good reasoning
ollama pull solar             # Terbaik tapi lambat

# Cara switch model:
# Edit: OLLAMA_MODEL = "mistral"
# Lalu: ollama pull mistral && streamlit run app.py
            """)
        
        st.divider()
        
        # Tip untuk user
        st.caption("""
        **Tips untuk Hasil Terbaik:**
        - Bertanya dengan spesifik dan detail
        - Gunakan kata kunci yang ada di dokumen
        - Tanya satu hal per pertanyaan
        - Tunggu hingga Ollama selesai (10-30 detik tergantung pertanyaan)
        - Jika timeout, coba pertanyaan lebih singkat
        """)

# ENTRY POINT - Jalankan aplikasi
if __name__ == "__main__":
    main()
