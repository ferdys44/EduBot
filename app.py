import streamlit as st
import google.generativeai as genai
import time

# Secrets otomatis
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    st.success("✅ **Gemini 2.5 Flash AKTIF!**")
except:
    st.error("❌ **Buat `.streamlit/secrets.toml` dulu!**")
    st.info("""
    1. GitHub → Add file → `.streamlit/secrets.toml`
    2. Isi: `GEMINI_API_KEY = "AIzaSyBETurylZKhvgJj1QhFNqj5hC9qr1exw60"`
    """)
    st.stop()

st.markdown("""
<style>
.chat-container { max-height: 60vh; overflow-y: auto; padding: 1rem; background: #f0f9ff; border-radius: 15px; border: 2px solid #0ea5e9; }
.msg { padding: 1rem; margin: 0.5rem 0; border-radius: 12px; }
.user { background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; }
.assistant { background: linear-gradient(135deg, #10b981, #059669); color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 **AI Tutor Akademik**")
st.markdown("**🧮 Matematika • ⚛️ Fisika • 🧪 Kimia • 🧬 Biologi**")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    msg_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(f'<div class="msg {msg_class}"><strong>{msg["role"].title()}:</strong> {msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Rate limit
if "last_chat" not in st.session_state:
    st.session_state.last_chat = 0

# Input
prompt = st.chat_input("💬 Tanyakan soal pelajaranmu... (Contoh: Hitung luas lingkaran r=7cm)")
if prompt and time.time() - st.session_state.last_chat > 2:
    st.session_state.last_chat = time.time()
    
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Assistant
    with st.chat_message("assistant"):
        with st.spinner("🤖 Gemini menjawab..."):
            try:
                # Prompt pintar
                system_prompt = f"""
Kamu GURU SMA AHLI semua pelajaran.
Jawab soal ini dengan:
1. **LANGKAH JELAS**
2. **RUMUS** + **HITUNGAN**
3. **JAWABAN AKHIR** bold

SOAL: {prompt}

FORMAT:
**🎯 SOAL:** ...
**📝 RUMUS:** ...
**🔢 HITUNG:** ...
**✅ JAWABAN:** ...
                """
                
                response = model.generate_content(system_prompt)
                answer = response.text
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
with col2:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

st.markdown("---")
st.caption("💎 Powered by Gemini 2.5 Flash | Gratis & Unlimited")
