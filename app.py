import streamlit as st
import boto3
import base64
import json

# --- GİZLİ SİSTEM AYARLARI ---
AGENT_ID = "J280YK35FY"
AGENT_ALIAS_ID = "IWAACDSX81" 
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

# Sayfa Yapılandırması
st.set_page_config(page_title="ZAKShield | Medikal Hukuk Savunma Sistemi", page_icon="🛡️", layout="wide")

# SES SİSTEMİ (Hata Gizleme Modu)
def sesli_yanit(metin):
    try:
        polly = boto3.client('polly', region_name=REGION, 
                             aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        response = polly.synthesize_speech(Text=metin[:1000], OutputFormat='mp3', VoiceId='Filiz')
        audio_content = response['AudioStream'].read()
        b64_audio = base64.b64encode(audio_content).decode()
        audio_html = f'<audio autoplay><source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)
    except:
        pass # Kullanıcıya hata gösterme, sessizce devam et.

# ÜST DÜZEY PRESTİJ TASARIMI
st.markdown("""
    <style>
    .main { background: #ffffff; }
    h1, h2, h3 { color: #0f172a !important; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #f1f5f9; }
    .stButton>button { 
        background: #1e293b; color: #fff !important; border-radius: 8px; font-weight: 700; height: 3.5em; border: none;
    }
    .stTextArea textarea { background-color: #f8fafc; border: 1px solid #e2e8f0; font-size: 16px; border-radius: 12px; }
    .card { padding: 20px; border-radius: 12px; border: 1px solid #f1f5f9; background: #ffffff; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# NAVİGASYON (Gelişmiş Menü)
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>ZAKShield</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("SİSTEM BÖLÜMLERİ", 
                    ["🏛️ Yönetim Paneli", "📊 Medikal Analiz Merkezi", "📂 Vaka Arşivi", "⚖️ Mevzuat Kütüphanesi", "👤 Kullanıcı Profili"])
    st.divider()
    st.write("**Oturum:** Dr. Ulaş Fırıncıoğulları")
    st.caption("Erişim Düzeyi: Kurumsal Premium")

# SAYFA 1: YÖNETİM PANELİ (DASHBOARD)
if menu == "🏛️ Yönetim Paneli":
    st.markdown("# 🏛️ Yönetim Paneli")
    st.markdown("##### Kliniğinizin hukuki güvenlik durumu ve istatistikleri.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown("<div class='card'><b>Toplam Analiz</b><br><span style='font-size:22px;'>247</span></div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='card'><b>Risk Skoru</b><br><span style='color:green; font-size:22px;'>Güvenli</span></div>", unsafe_allow_html=True)
    with col3: st.markdown("<div class='card'><b>Aktif Abonelik</b><br><span style='font-size:22px;'>Premium</span></div>", unsafe_allow_html=True)
    with col4: st.markdown("<div class='card'><b>Sistem Hızı</b><br><span style='font-size:22px;'>Turbo (C 4.5)</span></div>", unsafe_allow_html=True)
    
    st.markdown("### 🔔 Son Güncellemeler")
    st.info("📌 Kişisel Verileri Koruma Kurulu'nun sağlık verileriyle ilgili yeni kararı sisteme entegre edildi.")

# SAYFA 2: MEDİKAL ANALİZ MERKEZİ (ANA MOTOR)
elif menu == "📊 Medikal Analiz Merkezi":
    st.markdown("# 📊 Medikal Analiz Merkezi")
    st.markdown("##### Claude 4.5 motoru ile yüksek hassasiyetli risk taraması.")
    
    col_main, col_side = st.columns([3, 1])
    
    with col_main:
        vaka = st.text_area("Analiz Edilecek Vaka Notları veya Onam Formu:", height=450, placeholder="Hasta onam metnini veya vaka detaylarını buraya ekleyin...")
        if st.button("STRATEJİK ANALİZİ BAŞLAT"):
            if vaka:
                with st.spinner("ZAKShield Veri Tabanını Tarıyor..."):
                    try:
                        client = boto3.client(service_name='bedrock-agent-runtime', region_name=REGION,
                                            aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                        response = client.invoke_agent(agentId=AGENT_ID, agentAliasId=AGENT_ALIAS_ID, sessionId="zak_session", inputText=vaka)
                        
                        full_txt = ""
                        for event in response.get("completion"):
                            chunk = event.get("chunk")
                            if chunk: full_txt += chunk.get("bytes").decode()
                        
                        st.markdown("### 📋 Stratejik Analiz Raporu")
                        st.info(full_txt)
                        sesli_yanit(full_txt)
                    except:
                        st.error("Sistem şu an meşgul. Lütfen tekrar deneyin.")
            else:
                st.warning("Lütfen bir veri girişi yapın.")

    with col_side:
        st.markdown("### 🛡️ Analiz Kapsamı")
        st.markdown("- KVKK Uyumluluğu\n- Malpraktis Riskleri\n- Onam Eksiklikleri\n- Savunma Önerileri")

# SAYFA 3: VAKA ARŞİVİ
elif menu == "📂 Vaka Arşivi":
    st.markdown("# 📂 Vaka Arşivi")
    st.write("Geçmiş analizleriniz yüksek güvenlikli sunucularda saklanmaktadır.")
    st.dataframe({"Vaka ID": ["#901", "#900"], "Tarih": ["19.01.2026", "18.01.2026"], "Tür": ["Diş İmplant", "Komplikasyon"], "Durum": ["Tamamlandı", "Arşivlendi"]})

# SAYFA 4: MEVZUAT KÜTÜPHANESİ
elif menu == "⚖️ Mevzuat Kütüphanesi":
    st.markdown("# ⚖️ Mevzuat Kütüphanesi")
    st.markdown("##### Hekim Hakları ve Sağlık Mevzuatı Güncel Kayıtlar")
    st.write("- Tıbbi Deontoloji Nizamnamesi\n- Hasta Hakları Yönetmeliği\n- 6698 Sayılı KVKK")

# SAYFA 5: PROFİL
elif menu == "👤 Kullanıcı Profili":
    st.markdown("# 👤 Kullanıcı Profili")
    st.text_input("Ad Soyad", "Dr. Ulaş Fırıncıoğulları")
    st.text_input("Klinik Adı", "ZAKShield Medical")
    st.button("Profili Güncelle")

st.markdown("---")
st.caption("© 2026 ZAKShield AI | Professional Medical Defense System")
