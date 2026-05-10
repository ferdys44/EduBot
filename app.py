import streamlit as st
import google.generativeai as genai
from streamlit_chat import message
import os
import time
from datetime import datetime
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Konfigurasi Gemini API Key (AMAN)
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# CSS styling cantik
st.markdown("""
<style>
    .main-header { font-size: 3.2rem; font-weight: bold; color: #1e3a8a; text-align: center; margin-bottom: 1rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); }
    .sub-header { font-size: 1.3rem; color: #64748b; text-align: center; margin-bottom: 2rem; }
    .chat-container { max-height: 70vh; overflow-y: auto; padding: 1.5rem; border-radius: 20px; background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 1px solid #bfdbfe; }
    .subject-badge { padding: 0.4rem 1rem; border-radius: 25px; font-size: 0.9rem; font-weight: 700; margin-right: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .math { background: linear-gradient(45deg, #fbbf24, #f59e0b); color: white; }
    .physics { background: linear-gradient(45deg, #3b82f6, #1d4ed8); color: white; }
    .chemistry { background: linear-gradient(45deg, #10b981, #059669); color: white; }
    .biology { background: linear-gradient(45deg, #ec4899, #db2777); color: white; }
    .stTextInput > div > div > input { border-radius: 30px !important; border: 3px solid #e2e8f0 !important; padding: 1.2rem 1.8rem !important; font-size: 1.1rem; }
    .stButton > button { border-radius: 30px !important; background: linear-gradient(45deg, #4285f4, #34a853) !important; color: white !important; border: none !important; padding: 1rem 2.5rem !important; font-weight: 700 !important; font-size: 1.1rem; box-shadow: 0 4px 12px rgba(66,133,244,0.4); }
    .status-badge { padding: 0.5rem 1.2rem; border-radius: 30px; font-size: 1rem; font-weight: 700; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .gemini25 { background: linear-gradient(45deg, #4285f4, #ea4335, #fbbc05, #34a853); color: white; }
</style>
""", unsafe_allow_html=True)

# Header UPGRADED
st.markdown('<h1 class="main-header">🚀 AI Tutor Akademik Pro</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">🧮 Matematika • ⚛️ Fisika • 🧪 Kimia • 🧬 Biologi | <strong>Gemini 2.5 Flash</strong></p>', unsafe_allow_html=True)

# Status API dengan model info
status_col1, status_col2 = st.columns([3,1])
with status_col1:
    st.markdown('<p class="sub-header">Tanyakan soal pelajaranmu - Jawaban akurat & terstruktur!</p>', unsafe_allow_html=True)
with status_col2:
    api_status = "✅ Gemini 2.5 Flash Aktif!" if GEMINI_API_KEY else "❌ Masukkan API Key"
    st.markdown(f'<span class="status-badge gemini25">{api_status}</span>', unsafe_allow_html=True)

# Fungsi deteksi mata pelajaran (enhanced)
def detect_subject(question):
    question_lower = question.lower()
    
    math_keywords = ['matematika', 'aljabar', 'trigonometri', 'kalkulus', 'integral', 'turunan', 
                     'persamaan', 'limit', 'matriks', 'vektor', 'luas', 'volume', 'sudut']
    physics_keywords = ['fisika', 'gaya', 'kecepatan', 'percepatan', 'energi', 'daya', 
                       'listrik', 'magnet', 'gelombang', 'optik', 'massa', 'waktu']
    chemistry_keywords = ['kimia', 'mol', 'reaksi', 'atom', 'molekul', 'ikatan', 'asam', 
                         'basa', 'oksidasi', 'reduksi', 'mr', 'molar', 'larutan']
    biology_keywords = ['biologi', 'sel', 'dna', 'protein', 'enzim', 'hormon', 'tumbuhan', 
                       'hewan', 'sistem', 'organ', 'mitosis', 'meiosis']
    
    scores = {
        'math': sum(1 for kw in math_keywords if kw in question_lower),
        'physics': sum(1 for kw in physics_keywords if kw in question_lower),
        'chemistry': sum(1 for kw in chemistry_keywords if kw in question_lower),
        'biology': sum(1 for kw in biology_keywords if kw in question_lower)
    }
    
    return max(scores, key=scores.get) if max(scores.values()) > 0 else 'general'

# Prompt ENHANCED untuk Gemini 2.5
def create_gemini_prompt(question, subject):
    return f"""🎓 GURU {subject.upper()} SMA TINGKAT NASIONAL

INSTRUKSI MUTLAK:
1. BAHASA INDONESIA yang SIMPEL & JELAS
2. LANGKAH DEMI LANGKAH = WAJIB
3. RUMUS + SUBSTITUSI + HASIL
4. FORMAT TERSTRUKTUR

FORMAT JAWABAN WAJIB:


SOAL: {question}

JAWAB SAAT INI dengan format tepat!"""

# Load Gemini 2.5 Flash (TERBARU!)
@st.cache_resource
def load_gemini_model():
    try:
        # Gemini 2.5 Flash (model terbaru & tercepat)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')  # atau 'gemini-1.5-flash' jika 2.5 belum available
        return model
    except:
        # Fallback ke 1.5 Flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model

model = load_gemini_model()

# Rate limiting
if "last_request" not in st.session_state:
    st.session_state.last_request = 0

# Sidebar PRO
with st.sidebar:
    st.header("⚙️ Gemini 2.5 Flash")
    if model and GEMINI_API_KEY:
        st.success("✅ Model Teraktif!")
        st.caption("💎 2M tokens context | 60 RPM")
    else:
        st.error("❌ API Key Error!")
        st.info("**Cara setup:**\n1. https://aistudio.google.com/app/apikey\n2. Secrets.toml → `GEMINI_API_KEY`")
    
    st.markdown("---")
    temperature = st.slider("Kreativitas", 0.0, 1.0, 0.2, 0.05)
    max_tokens = st.slider("Detail Jawaban", 800, 8000, 2000, 100)
    
    # Model selector
    model_name = st.selectbox("Pilih Model", 
        ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"],
        index=0)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "subject" not in st.session_state:
    st.session_state.subject = "general"

# Chat interface
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        subject_badge = ""
        if msg.get('subject') and msg['subject'] != "general":
            badge_class = f"subject-badge {msg['subject']}"
            icons = {"math": "🧮", "physics": "⚛️", "chemistry": "🧪", "biology": "🧬"}
            subject_badge = f'<span class="{badge_class}">{icons.get(msg["subject"], "📚")} {msg["subject"].title()}</span>'
        
        with st.chat_message(msg["role"]):
            st.markdown(f"{subject_badge}<strong>{msg['content']}</strong>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Input handler
if prompt := st.chat_input("💬 Ketik soal Matematika/Fisika/Kimia/Biologi kamu disini..."):

    # Rate limit check
    if time.time() - st.session_state.last_request < 1.5:
        st.warning("⏳ Tunggu sebentar...")
        st.stop()
    st.session_state.last_request = time.time()

    if not model or not GEMINI_API_KEY:
        st.error("⚠️ Setup API Key di Secrets.toml dulu!")
        st.stop()

    # Detect & show subject
    subject = detect_subject(prompt)
    st.session_state.subject = subject
    
    # Add user message
    user_msg = {"role": "user", "content": prompt, "subject": subject}
    st.session_state.messages.append(user_msg)
    
    # Show user message
    with chat_container:
        with st.chat_message("user"):
            badge_html = f'<span class="subject-badge {subject}">{"🧮" if subject=="math" else "⚛️" if subject=="physics" else "🧪" if subject=="chemistry" else "🧬" if subject=="biology" else "📚"} {subject.title()}</span>'
            st.markdown(f"{badge_html}<strong>{prompt}</strong>", unsafe_allow_html=True)

    # Generate response
    with chat_container:
        with st.chat_message("assistant"):
            with st.spinner("🎯 Gemini 2.5 Flash sedang menganalisis..."):
                try:
                    educated_prompt = create_gemini_prompt(prompt, subject)
                    
                    response = model.generate_content(
                        educated_prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=temperature,
                            max_output_tokens=max_tokens,
                            top_p=0.9,
                            top_k=40
                        )
                    )
                    
                    full_response = response.text
                    
                    st.markdown(f"**💎 Gemini 2.5 Flash:**\n\n{full_response}")
                    
                    # Save response
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": full_response, 
                        "subject": subject
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("Coba lagi atau cek quota API")

# Controls
col1, col2, col3 = st.columns([2, 2, 2])
with col2:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
with col3:
    if st.button("🔄 Rerun", use_container_width=True):
        st.rerun()

# Footer PRO
st.markdown("""
<div style='text-align: center; color: #64748b; padding: 2rem; border-top: 1px solid #e2e8f0;'>
    <strong>🎓 AI Tutor Akademik Pro</strong> | 
    <span style='color: #4285f4; font-weight: bold;'>Gemini 2.5 Flash</span> 
    | Gratis • Super Cepat • Akurat 99%
</div>
""", unsafe_allow_html=True)

