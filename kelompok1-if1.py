import streamlit as st
import pandas as pd
import os

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Dashboard Bike Sharing - Kelompok 1",
    page_icon="🚲",
    layout="wide"
)

# --- 2. FUNGSI LOAD DATA (LANGSUNG CSV) ---
@st.cache_data
def load_data():
    # Pastikan file 'day_updated.csv' ada di folder yang sama dengan skrip ini
    file_path = "day_updated.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return None

df = load_data()

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("Menu Dashboard")
menu = st.sidebar.radio(
    "Pilih Halaman:",
    ["Beranda", "Tabel Data", "Analisis Musim", "Statistik Penyewa", "Tentang Kami"]
)

# --- 4. LOGIKA HALAMAN ---

if df is not None:
    if menu == "Beranda":
        st.title("🚲 Analisis Data: Bike-sharing-dataset")
        st.subheader("Kelompok 1 - IF1")
        st.write("Dashboard ini menampilkan hasil analisis penyewaan sepeda berdasarkan data harian yang telah diperbarui.")
        
        # Ringkasan Statistik Utama (KPI)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Hari", len(df))
        with col2:
            st.metric("Total Penyewa", f"{df['Total Penyewa'].sum():,}")
        with col3:
            st.metric("Rata-rata/Hari", f"{int(df['Total Penyewa'].mean())}")

    elif menu == "Tabel Data":
        st.title("📋 Cek Data")
        st.write("Menampilkan dataset lengkap dari file CSV.")
        st.dataframe(df, use_container_width=True)

    elif menu == "Analisis Musim":
        st.title("🌤️ Filter Berdasarkan Musim")
        # Pilihan Musim dari data unik
        musim_list = df['Musim'].unique()
        selected_musim = st.selectbox("Pilih Musim yang Ingin Dilihat:", musim_list)
        
        # Filter Data
        filtered_df = df[df['Musim'] == selected_musim]
        st.write(f"Menampilkan {len(filtered_df)} baris data untuk musim **{selected_musim}**.")
        st.dataframe(filtered_df, use_container_width=True)
        
        # Grafik Tren harian untuk musim terpilih
        st.line_chart(filtered_df.set_index('Tanggal')['Total Penyewa'])

    elif menu == "Statistik Penyewa":
        st.title("📊 Statistik Total Penyewa per Musim")
        
        # Menggunakan Tabs untuk memisahkan kategori statistik
        tab1, tab2, tab3, tab4 = st.tabs(["Total", "Rata-rata", "Maksimal", "Minimal"])
        
        with tab1:
            st.write("### Total Penyewa per Musim")
            # Menghitung total penyewa per musim
            res_sum = df.groupby("Musim")["Total Penyewa"].sum().reset_index()
            # Menampilkan tabel secara penuh (full width)
            st.table(res_sum)

        with tab2:
            st.write("### Rata-rata Penyewa per Musim")
            # Menghitung rata-rata penyewa per musim
            res_avg = df.groupby("Musim")["Total Penyewa"].mean().reset_index()
            res_avg.columns = ["Musim", "Rata-rata Penyewa"]
            st.table(res_avg)

        with tab3:
            st.write("### Jumlah Penyewa Terbanyak (Max)")
            # Mencari nilai maksimal per musim
            res_max = df.groupby("Musim")["Total Penyewa"].max().reset_index()
            st.table(res_max)

        with tab4:
            st.write("### Jumlah Penyewa Tersedikit (Min)")
            # Mencari nilai minimal per musim
            res_min = df.groupby("Musim")["Total Penyewa"].min().reset_index()
            st.table(res_min)
    elif menu == "Tentang Kami":
        st.title("👥 Tentang Kami")
        st.write("""
        **Kelompok 1 - IF1**  
        Anggota Kelompok:  
        - Anggota 1  Imran Dika Awwaludin   (10124022)
        - Anggota 2  Willy Wildan Hapid     (10124023)
        - Anggota 3 Muhamad Nurdin          (10124024)
        - Anggota 4  Ian Kurniawan          (10124031)
        - Anggota 5  Diky Hidayat           (10124030)
        - Anggota 6  Aditya Elfian Susanto  (10124014)
        
        Proyek ini bertujuan untuk menganalisis data penyewaan sepeda menggunakan dataset harian yang telah diperbarui.
        """)