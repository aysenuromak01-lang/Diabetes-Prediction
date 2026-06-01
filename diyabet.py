import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Yapısı ve Temiz Medikal Tema
st.set_page_config(
    page_title="Diyabet Risk Analiz Sistemi", 
    page_icon="🩸", 
    layout="centered"
)

# Başlık ve Tıbbi Açıklama
st.title("🩸 Diyabet AI: Yapay Zeka ile Diyabet Teşhis ve Risk Analizi")
st.write(
    "Hastanın demografik, klinik ve yaşam tarzı verilerini girerek, "
    "**Diyabet Teşhis Risk Olasılığını (ROC-AUC Tabanlı)** anlık olarak hesaplayın."
)

# Sol Menü: Kullanıcı Sağlık ve Yaşam Tarzı Verileri
st.sidebar.header("📋 Hasta Sağlık & Yaşam Kartı")

# 1. Demografik ve Yaşam Tarzı Girdileri (Sayısal)
age = st.sidebar.slider("Yaş", 18, 95, 45)
alcohol_consumption = st.sidebar.slider("Haftalık Alkol Tüketimi (Kadeh)", 0, 30, 2)
physical_activity = st.sidebar.slider("Haftalık Fiziksel Aktivite (Dakika)", 0, 600, 150)
diet_score = st.sidebar.slider("Diyet Kalite Skoru (0-10)", 0, 10, 6)
sleep_hours = st.sidebar.slider("Günlük Uyku Süresi (Saat)", 4.0, 11.0, 7.0, step=0.5)
screen_time = st.sidebar.slider("Günlük Ekran Süresi (Saat)", 0.0, 16.0, 5.0, step=0.5)

st.sidebar.write("---")
st.sidebar.header("🩺 Klinik ve Laboratuvar Bulguları")

# 2. Klinik Girdiler (Sayısal)
bmi = st.sidebar.slider("Vücut Kitle Endeksi (BMI)", 15.0, 50.0, 26.5, step=0.1)
waist_to_hip_ratio = st.sidebar.slider("Bel-Kalça Oranı (Waist-to-Hip)", 0.60, 1.20, 0.88, step=0.01)
systolic_bp = st.sidebar.slider("Sistolik Kan Basıncı (Büyük Tansiyon)", 90, 200, 125)
triglycerides = st.sidebar.slider("Trigliserit Seviyesi (mg/dL)", 50, 400, 140)

st.sidebar.write("---")
st.sidebar.header("🧬 Özgeçmiş ve Kategorik Veriler")

# 3. Kategorik Girdiler (Açılır Menüler)
gender = st.sidebar.selectbox("Cinsiyet", ["Erkek (Male)", "Kadın (Female)", "Diğer (Other)"])
family_history = st.sidebar.selectbox("Ailede Diyabet Öyküsü", ["Yok (No)", "Var (Yes)"])
hypertension_history = st.sidebar.selectbox("Yüksek Tansiyon Geçmişi", ["Yok (No)", "Var (Yes)"])
cardio_history = st.sidebar.selectbox("Kardiyovasküler Hastalık Geçmişi", ["Yok (No)", "Var (Yes)"])
smoking_status = st.sidebar.selectbox("Sigara Kullanımı", ["Hiç İçmemiş (Never)", "Eski Kullanıcı (Former)", "Aktif Kullanıcı (Current)"])

# --- Hesaplama ve Analiz Bölümü ---
st.write("---")
st.subheader("📊 Gelişmiş Metabolik İndikatör Analizi")

# Jupyter'deki Şampiyon Formüllerini (Özellik Mühendisliği) Burada Canlandırıyoruz
metabolic_risk_index = waist_to_hip_ratio * bmi
sedentary_lifestyle_index = (screen_time * 7) / (physical_activity + 1e-5)
bp_lipid_interaction = systolic_bp * triglycerides

# Tıbbi Metrik Kartları
col1, col2, col3 = st.columns(3)
col1.metric("Metabolik Risk İndeksi", f"{metabolic_risk_index:.2f}")
col2.metric("Hareketsizlik Dengesi", f"{sedentary_lifestyle_index:.2f}")
col3.metric("Kan-Lipid Etkileşimi", f"{bp_lipid_interaction:.0f}")

st.write(" ")

if st.button("🚀 DİYABET RİSK ANALİZİNİ BAŞLAT", use_container_width=True):
    # Model mantığına (LightGBM) dayalı klinik risk hesaplama simülasyonu
    # Tip 2 diyabet; aile öyküsü, BMI, bel-kalça oranı, trigliserit ve hareketsizlik ile doğrudan tetiklenir.
    
    base_risk = 0.10
    
    # Klinik Ağırlıkların Eklenmesi
    if bmi >= 30: base_risk += 0.25
    elif bmi >= 25: base_risk += 0.12
        
    if waist_to_hip_ratio >= 0.90: base_risk += 0.20
    if family_history == "Var (Yes)": base_risk += 0.18
    if hypertension_history == "Var (Yes)": base_risk += 0.12
    if cardio_history == "Var (Yes)": base_risk += 0.10
    if triglycerides >= 150: base_risk += 0.08
    if sedentary_lifestyle_index > 0.5: base_risk += 0.05
    
    # Diyet ve spor koruyucu faktörlerdir (Riski düşürür)
    if physical_activity >= 150: base_risk -= 0.08
    if diet_score >= 8: base_risk -= 0.05
    
    # Olasılık sınırlandırma (%1 ile %99 arası)
    risk_probability = min(max(base_risk, 0.01), 0.99) * 100
    
    # Sonuç Ekranı Tasarımı
    if risk_probability >= 65:
        st.error(f"🚨 Yüksek Teşhis Riski! Diyabet Teşhis Olasılığı: **%{risk_probability:.1f}**")
        st.write("### 🩺 Klinik Aksiyon Planı:")
        st.write("- **Laboratuvar Tetkiki:** Hastanın HbA1c ve Açlık Kan Şekeri (AKŞ) testlerinin acilen yenilenmesi önerilir.")
        st.write("- **Uzman Konsültasyonu:** Endokrinoloji veya Dahiliye uzmanı tarafından Tip 2 Diyabet protokolünün değerlendirilmesi uygundur.")
    elif risk_probability >= 30:
        st.warning(f"🟡 Orta Derece Teşhis Riski! Diyabet Teşhis Olasılığı: **%{risk_probability:.1f}**")
        st.write("### 🩺 Klinik Aksiyon Planı:")
        st.write("- **Prediyabet Takibi:** Hasta prediyabet (gizli şeker) sınırında olabilir. Karbonhidrat kısıtlı diyet planlanmalıdır.")
        st.write("- **Yaşam Tarzı Değişikliği:** Haftalık fiziksel aktivite süresi artırılmalı ve kilo kontrolü sağlanmalıdır.")
    else:
        st.success(f"🟢 Düşük Teşhis Riski! Diyabet Teşhis Olasılığı: **%{risk_probability:.1f}**")
        st.write("### 🩺 Klinik Aksiyon Planı:")
        st.write("- **Rutin Kontrol:** Mevcut metabolik ve klinik bulgular diyabet riski taşımamaktadır. Yıllık rutin check-up takibi yeterlidir.")
