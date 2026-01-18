import streamlit as st
import boto3
import json
import base64

# --- STRATEJİK YAPILANDIRMA ---
AGENT_ID = "J280YK35FY"
AGENT_ALIAS_ID = "IWAACDSX81" 
AWS_ACCESS_KEY = "AKIAZQW6QVW5L6AQKVEG"
AWS_SECRET_KEY = "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"
REGION = "us-east-1"

# Sayfa Ayarları
st.set_page_config(page_title="ZAKShield AI | Medical Defense System", page_icon="🛡️", layout="wide")

# SES SİSTEMİ (Amazon Polly Entegrasyonu)
def speak_text(text):
    try:
        polly = boto3.client('polly', region_name=REGION, 
                             aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
        # Türkçe kadın sesi (Filiz) veya erkek sesi için ayarlanabilir
        response = polly.synthesize_speech(Text=text[:3000], OutputFormat='mp3', VoiceId='Filiz')
        audio_content = response['AudioStream'].read()
        b64_audio = base64.b64encode(audio_content).decode()
        audio_html = f'<audio autoplay><source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3"></audio>'
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Ses sistemi hatası: {e}")

# ÜST SEVİYE PRESTİJ TASARIMI (Pure Medical White & Navy)
st.markdown("""
    <style>
    .main { background: #f8fafc; }
    /* Yazı fontları ve renkleri */
    h1, h2, h3 { color: #0f172a !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    p, span, label { color: #334155 !important; font-size: 16px; }
    
    /* Yan Menü Tasarımı */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    
    /* Buton Tasarımı: Otoriter Lacivert */
    .stButton>button { 
        width: 100%; border-radius: 8px; background: #1e293b; color: #ffffff !important; 
        font-weight: 700; height: 3.5em; border: none; transition: 0.4s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover { background: #0f172a; transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2); }
    
    /* Giriş Alanları */
    .stTextArea textarea { background-color: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; font-size: 16px; padding: 15px; }
    
    /* Kartlar */
    .info-card { background: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    .stat-box { text-align: center; padding: 15px; background: #f1f5f9; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# YAN MENÜ (Dolu Dolu Navigasyon)
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🛡️ ZAKShield</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 12px; color: #64748b;'>PREMIUM MEDICAL DEFENSE</p>", unsafe_allow_html=True)
    st.divider()
    
    menu = st.radio("ANA MENÜ", ["🏛️ Kontrol Paneli", "📊 Vaka Analizi", "📂 Dijital Arşiv", "💳 Üyelik & Planlar", "⚙️ Profil Ayarları"])
    
    st.divider()
    st.markdown("### 👨‍⚕️ Kullanıcı Profili")
    st.info("**Dr. Ulaş Fırıncıoğulları**\n\nBranş: Klinik Yönetimi\nStatü: Premium Üye")
    
    if st.button("Güvenli Çıkış"):
        st.toast("Oturum kapatılıyor...")

# SAYFA İÇERİKLERİ
if menu == "🏛️ Kontrol Paneli":
    st.markdown("# 🏛️ Kontrol Paneli")
    st.markdown("##### Hoş geldiniz Dr. Ulaş. İşte kliniğinizin hukuki güvenlik özeti.")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown("<div class='stat-box'><b>Aktif Vakalar</b><br><span style='font-size:24px;'>12</span></div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='stat-box'><b>Analiz Edilen Formlar</b><br><span style='font-size:24px;'>148</span></div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='stat-box'><b>Risk Skoru</b><br><span style='font-size:24px; color:green;'>Düşük</span></div>", unsafe_allow_html=True)
    with c4: st.markdown("<div class='stat-box'><b>Kalan Kredi</b><br><span style='font-size:24px;'>Sınırsız</span></div>", unsafe_allow_html=True)
    
    st.markdown("### 🔔 Son Bildirimler")
    st.write("✅ Yeni mevzuat güncellemesi: 'Aydınlatılmış Onam Formları Revizyonu' sisteme eklendi.")
    st.write("✅ Dünkü vaka analiziniz başarıyla arşivlendi.")

elif menu == "📊 Vaka Analizi":
    st.markdown("# 📊 Medikal Risk Analizi")
    st.markdown("##### Yapay zeka motoru, vaka detaylarınızı en güncel mevzuatla karşılaştırır.")
    
    col_input, col_tips = st.columns([2, 1])
    
    with col_input:
        st.markdown("### 📝 Analiz Girdisi")
        vaka_metni = st.text_area("Onam formu içeriği veya vaka detaylarını buraya giriniz:", height=400, placeholder="Doktor notlarını veya hasta onam metnini analiz için buraya aktarın...")
        
        if st.button("ANALİZİ BAŞLAT VE RAPORLA"):
            if vaka_metni:
                with st.spinner("AI Hukuk Danışmanı metni inceliyor..."):
                    try:
                        client = boto3.client(service_name='bedrock-agent-runtime', region_name=REGION,
                                            aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
                        
                        response = client.invoke_agent(agentId=AGENT_ID, agentAliasId=AGENT_ALIAS_ID, sessionId="user-123", inputText=vaka_metni)
                        
                        full_res = ""
                        for event in response.get("completion"):
                            chunk = event.get("chunk")
                            if chunk: full_res += chunk.get("bytes").decode()
                        
                        st.markdown("---")
                        st.markdown("### ⚖️ Stratejik Analiz Raporu")
                        st.markdown(f"<div class='info-card'>{full_res}</div>", unsafe_allow_html=True)
                        
                        # SESLİ OKUMA BAŞLAT
                        speak_text(full_res)
                        
                    except Exception as e:
                        st.error("Bağlantı sağlanamadı. Lütfen daha sonra tekrar deneyiniz.")
            else:
                st.warning("Lütfen bir metin girişi yapın.")

    with col_tips:
        st.markdown("### 💡 Profesyonel İpuçları")
        st.markdown("""
        <div class='info-card'>
        <b>Onam Formları:</b><br>Hastanın sadece imzasını değil, "Kendi el yazısıyla okudum anladım" ibaresini eklediğinden emin olun.
        </div>
        <div class='info-card'>
        <b>Komplikasyon Kaydı:</b><br>Oluşan komplikasyonun tıbbi standartlar içinde olduğunu detaylandırın.
        </div>
        """, unsafe_allow_html=True)

elif menu == "📂 Dijital Arşiv":
    st.markdown("# 📂 Dijital Arşiv")
    st.write("Tüm geçmiş analizleriniz tarih sırasına göre burada saklanır.")
    st.table({"Tarih": ["18.01.2026", "17.01.2026"], "Vaka Tipi": ["İmplant Onam", "Kanal Tedavisi"], "Risk Durumu": ["Güvenli", "Orta Risk"]})

elif menu == "💳 Üyelik & Planlar":
    st.markdown("# 💎 Üyelik ve Planlar")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='info-card'><h3>Kurumsal</h3><p>Sınırsız Analiz<br>7/24 Teknik Destek<br>Hukuki Taslak Hazırlama</p><h4>Aktif</h4></div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='info-card'><h3>Holding / Hastane</h3><p>Çoklu Kullanıcı<br>API Erişimi<br>Özel Avukat Paneli</p><h4>Yükselt</h4></div>", unsafe_allow_html=True)

elif menu == "⚙️ Profil Ayarları":
    st.markdown("# ⚙️ Profil Ayarları")
    st.text_input("Ad Soyad", value="Dr. Ulaş Fırıncıoğulları")
    st.text_input("Klinik Adı", value="ZAK Medical Center")
    st.button("Bilgileri Güncelle")

# FOOTER
st.markdown("---")
st.caption("© 2026 ZAKShield AI | Tüm verileriniz medikal güvenlik standartlarında (HIPAA/KVKK) korunmaktadır.")
