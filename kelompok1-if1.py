import streamlit as st
import pandas as pd
import os
from streamlit_option_menu import option_menu

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================== CUSTOM CSS (ADAPTIVE & UI TETAP) =====================
st.markdown("""
<style>
    /* HILANGKAN TOMBOL DEPLOY */
    .stDeployButton { display: none; }

    /* KONFIGURASI WARNA ADAPTIF */
    :root {
        --card-bg: var(--secondary-background-color);
        --main-text: var(--text-color);
    }

    /* HEADER TRANSPARAN */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }

    /* TOPBAR */
    .topbar {
        background: var(--card-bg);
        padding: 15px 25px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 6px solid #4e73df;
        color: var(--main-text);
    }

    /* KPI CARDS */
    .kpi-card {
        background: var(--card-bg);
        color: var(--main-text);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #4e73df;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .kpi-card:hover { transform: translateY(-5px); }
    
    .kpi-title { font-size: 13px; font-weight: 700; text-transform: uppercase; opacity: 0.7; }
    .kpi-value { font-size: 26px; font-weight: 800; margin-top: 5px; }

    /* Warna Border KPI */
    .border-blue { border-left-color: #4e73df; }
    .border-green { border-left-color: #1cc88a; }
    .border-yellow { border-left-color: #f6c23e; }
    .border-red { border-left-color: #e74a3b; }

    /* CONTENT CARD */
    .content-card {
        background: var(--card-bg);
        color: var(--main-text);
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .content-card h4 { color: #4e73df !important; margin-bottom: 20px; }
    
    /* FOOTER */
    .footer {
        text-align: center; color: var(--main-text); opacity: 0.5;
        font-size: 13px; margin-top: 50px;
        border-top: 1px solid rgba(128,128,128,0.2); padding-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ===================== LOAD DATA =====================
@st.cache_data
def load_data():
    file_path = "day_updated.csv"
    if os.path.exists(file_path):
        data = pd.read_csv(file_path)
        # Pastikan kolom tanggal menjadi tipe datetime untuk analisis RFM
        if 'Tanggal' in data.columns:
            data['Tanggal'] = pd.to_datetime(data['Tanggal'])
        return data
    return None

df = load_data()

# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown(f"<h2 style='text-align: center; color: var(--text-color);'>🚲 Bike Admin</h2>", unsafe_allow_html=True)
    
    menu = option_menu(
        menu_title=None,
        options=["Dashboard", "Dataset", "Analisis Musim", "RFM Analysis", "Tentang Kami"],
        icons=["speedometer2", "table", "cloud-sun", "activity", "people-fill"], 
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "var(--background-color)"},
            "icon": {"color": "#f6c23e", "font-size": "18px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"5px", "color": "var(--text-color)"},
            "nav-link-selected": {"background-color": "#4e73df"},
        }
    )
    
    # FOOTER SIDEBAR TETAP DI BAWAH
    st.markdown(f"""
    <div style="
        margin-top: 240px;
        text-align: center;
        font-size: 12px;
        color: var(--text-color);
        opacity: 0.5;
        border-top: 2px solid rgba(128,128,128,0.2);
        padding-top: 10px;
    ">
        Kelompok 1 - IF1 © 2026
    </div>
    """, unsafe_allow_html=True)

# ===================== TOPBAR =====================
st.markdown(f"""
<div class="topbar">
    <div>
        <div style="font-size: 22px; font-weight: bold; color: #4e73df;">Bike Sharing Analytics</div>
        <div style="font-size: 13px; opacity: 0.8;">Halaman Aktif: <b>{menu}</b></div>
    </div>
    <div style="text-align:right; font-weight:500;">
        Welcome, Admin! 👋
    </div>
</div>
""", unsafe_allow_html=True)

# ===================== PAGE CONTENT =====================
if df is not None:

    # --- DASHBOARD ---
    if menu == "Dashboard":
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown(f'<div class="kpi-card border-blue"><div class="kpi-title">Total Hari</div><div class="kpi-value">{len(df)}</div></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div class="kpi-card border-green"><div class="kpi-title">Total Penyewa</div><div class="kpi-value">{df["Total Penyewa"].sum():,}</div></div>', unsafe_allow_html=True)
        with col3: st.markdown(f'<div class="kpi-card border-yellow"><div class="kpi-title">Rata-rata / Hari</div><div class="kpi-value">{int(df["Total Penyewa"].mean()):,}</div></div>', unsafe_allow_html=True)
        with col4: st.markdown(f'<div class="kpi-card border-red"><div class="kpi-title">Penyewa Maks</div><div class="kpi-value">{df["Total Penyewa"].max():,}</div></div>', unsafe_allow_html=True)

        colA, colB = st.columns([2, 1])
        with colA:
            st.markdown('<div class="content-card"><h4>📈 Tren Penyewa Harian</h4>', unsafe_allow_html=True)
            st.line_chart(df.set_index("Tanggal")["Total Penyewa"], color="#4e73df")
            st.markdown('</div>', unsafe_allow_html=True)
        with colB:
            st.markdown('<div class="content-card"><h4>🍂 Distribusi Musim</h4>', unsafe_allow_html=True)
            season_sum = df.groupby("Musim")["Total Penyewa"].sum()
            st.bar_chart(season_sum, color="#1cc88a")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- DATASET ---
    elif menu == "Dataset":
        st.markdown('<div class="content-card"><h4>📦 Raw Dataset</h4>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ANALISIS MUSIM ---
    elif menu == "Analisis Musim":
        st.markdown('<div class="content-card"><h4>⛅ Analisis Per Musim</h4>', unsafe_allow_html=True)
        selected_musim = st.selectbox("Pilih Musim:", df["Musim"].unique())
        filtered_df = df[df["Musim"] == selected_musim]
        st.area_chart(filtered_df.set_index("Tanggal")["Total Penyewa"], color="#f6c23e")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ANALISIS LANJUTAN: RFM ---
    elif menu == "RFM Analysis":
        st.markdown('<div class="content-card"><h4>🚀 RFM Analysis (Advanced Analysis)</h4>', unsafe_allow_html=True)
        st.info("RFM Analysis mengukur performa berdasarkan waktu (Recency), frekuensi (Frequency), dan jumlah penyewa (Monetary).")
        
        # Perhitungan RFM sederhana berdasarkan Musim
        rfm_df = df.groupby(by="Musim", as_index=False).agg({
            "Tanggal": "max", 
            "Total Penyewa": ["count", "sum"]
        })
        rfm_df.columns = ["Musim", "Max_Date", "Frequency", "Monetary"]
        latest_date = df["Tanggal"].max()
        rfm_df["Recency (days)"] = (latest_date - rfm_df["Max_Date"]).dt.days
        
        tab_r, tab_f, tab_m = st.tabs(["Recency", "Frequency", "Monetary"])
        with tab_r:
            st.bar_chart(rfm_df.set_index("Musim")["Recency (days)"], color="#e74a3b")
        with tab_f:
            st.bar_chart(rfm_df.set_index("Musim")["Frequency"], color="#4e73df")
        with tab_m:
            st.bar_chart(rfm_df.set_index("Musim")["Monetary"], color="#1cc88a")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- ABOUT ---
    elif menu == "Tentang Kami":
        st.markdown("""
        <div class="content-card">
            <h3>👨‍💻 Tim Pengembang Kelompok 1 - IF1</h3>
            <ul style="line-height: 1.8;">
                <li>Imran Dika Awwaludin (10124022)</li>
                <li>Willy Wildan Hapid (10124023)</li>
                <li>Muhamad Nurdin (10124024)</li>
                <li>Ian Kurniawan (10124031)</li>
                <li>Diky Hidayat (10124030)</li>
                <li>Aditya Elfian Susanto (10124014)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # FOOTER UTAMA
    st.markdown("""
    <div class="footer">
        © 2026 Bike Sharing Dashboard | Integrated Analytics | Kelompok 1 IF-1
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("❌ File 'day_updated.csv' tidak ditemukan.")