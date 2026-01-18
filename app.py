import streamlit as st
import boto3
import base64
import json

# --- SİSTEM PARAMETRELERİ ---
AGENT_ID = "J280YK35FY"
AGENT_ALIAS_ID = "IWAACDSX81" 
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

st.set_page_config(page_title="ZAKShield AI | Medical Legal Intel", page_icon="🛡️", layout="wide")

# SESLENDİRME MOTORU (Amazon Polly)
def seslendir(metin):
    try:
        polly = boto3.client('polly', region_name=REGION, 
                             aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        response = polly.synthesize_speech(Text=metin[:800], OutputFormat='mp3', VoiceId='Filiz')
        audio_content = response['AudioStream'].read()
        b64_audio = base64.b64encode(audio_content).decode()
        audio_html = f'<audio autoplay><source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)
    except:
        pass 

# PRESTİJLİ GÖRSEL TASARIM
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1, h2, h3 { color: #0f172a !important; font-family: 'Inter', sans-serif; }
    .stButton>button { 
        background: #1e293b; color: #fff !important; border-radius: 6px; font-weight: 700; height: 3.5em; border: none;
    }
    [data-testid="stSidebar"] { background: #f8fafc; border-right: 1px solid #e2e8f0; }
    .card { padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; background: #fff; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# NAVİGASYON
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🛡️ ZAKShield</h2>", unsafe_allow_html=True)
    st.divider()
    menu = st.radio("OPERASYON MERKEZİ", 
                    ["🏛️ Yönetim Paneli", "📊 Vaka Analiz Merkezi", "📜 Savunma Robotu", "📁 Vaka Arşivi", "👤 Hekim Profili"])
    st.divider()
    st.info("**Oturum:** Dr. Ulaş Fırıncıoğulları")
    st.caption("Erişim: Kurumsal Premium")

# --- DASHBOARD ---
if menu == "🏛️ Yönetim Paneli":
    st.markdown("# 🏛️ Yönetim Paneli")
    st.markdown("##### Hoş geldiniz Dr. Ulaş. Kliniğinizin hukuki güvenlik özeti.")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='card'><b>Toplam Analiz</b><br>312</div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='card'><b>Risk Skoru</b><br><span style='color:green'>Minimal</span></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='card'><b>Abonelik</b><br>Aktif</div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='card'><b>AI Motoru</b><br>C 4.5</div>", unsafe_allow_html=True)
    
    st.markdown("### 🔔 Son Güncellemeler")
    st.success("✅ Yargıtay'ın son malpraktis kararları analiz motoruna entegre edildi.")

# --- ANALİZ MERKEZİ ---
elif menu == "📊 Vaka Analiz Merkezi":
    st.markdown("# 📊 Medikal Analiz Merkezi")
    vaka = st.text_area("Vaka Notları veya Onam Formu:", height=400, placeholder="Analiz edilecek içeriği buraya aktarın...")
    if st.button("ANALİZİ BAŞLAT"):
        if vaka:
            with st.spinner("AI Hukuk Danışmanı İnceliyor..."):
                try:
                    client = boto3.client(service_name='bedrock-agent-runtime', region_name=REGION,
                                        aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                    response = client.invoke_agent(agentId=AGENT_ID, agentAliasId=AGENT_ALIAS_ID, sessionId="live-session", inputText=vaka)
                    res = "".join([e.get("chunk").get("bytes").decode() for e in response.get("completion") if e.get("chunk")])
                    st.markdown("### ⚖️ Stratejik Analiz Raporu")
                    st.info(res)
                    seslendir(res)
                except:
                    st.error("Bağlantı şu an yoğun. Lütfen tekrar deneyiniz.")
        else:
            st.warning("Lütfen bir metin girişi yapın.")

# --- SAVUNMA ROBOTU ---
elif menu == "📜 Savunma Robotu":
    st.markdown("# 📜 Savunma Robotu")
    st.write("Olası bir şikayet durumunda ön savunma taslağı hazırlayın.")
    vaka_tipi = st.selectbox("Vaka Tipi", ["Cerrahi Komplikasyon", "Aydınlatma Eksikliği", "Beklenen Risk"])
    if st.button("Taslak Oluştur"):
        st.write("Savunma taslağı AI tarafından hazırlanıyor...")

# --- ARŞİV ---
elif menu == "📁 Vaka Arşivi":
    st.markdown("# 📁 Vaka Arşivi")
    st.table({"ID": ["#210", "#209"], "Tarih": ["19.01.2026", "18.01.2026"], "Tür": ["İmplant", "Kanal"], "Risk": ["Güvenli", "Orta"]})

# --- PROFİL ---
elif menu == "👤 Hekim Profili":
    st.markdown("# 👤 Hekim Profili")
    st.text_input("Ad Soyad", "Dr. Ulaş Fırıncıoğulları")
    st.text_input("Klinik Adı", "ZAKShield Medical Center")
    st.button("Profili Güncelle")

st.markdown("---")
st.caption("© 2026 ZAKShield AI | Professional Medical-Legal Defense")
