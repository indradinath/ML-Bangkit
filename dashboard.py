import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


def load_data_day(file_path):
    """Load day data from CSV."""
    day_df = pd.read_csv(file_path)
    return day_df

def load_data_hour(file_path):
    """Load hour data from CSV."""
    hour_df = pd.read_csv(file_path)
    return hour_df

# Memuat data
day_df = load_data_day('day_cleaned.csv')
hour_df = load_data_hour('hour_cleaned.csv')

# Menampilkan informasi dasar
print(day_df.head())
print(hour_df.head())

# Load DataFrame dari berkas yang telah dibersihkan
all_df = pd.read_csv('day_cleaned.csv')

# Kolom 'dteday' diubah ke tipe tanggal
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

# Mendapatkan tanggal minimum dan maksimum
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

# Sidebar untuk filter dan logo
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
         min_value=min_date.date(),  # Mengambil nilai .date() agar sesuai dengan tipe
        max_value=max_date.date(),
        value=(min_date.date(), max_date.date())  # Mengatur nilai default
    )

# Mengonversi start_date dan end_date ke datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Memfilter DataFrame berdasarkan rentang tanggal yang dipilih
filtered_data = all_df[(all_df['dteday'] >= start_date) & (all_df['dteday'] <= end_date)]

# Menampilkan data yang telah difilter
st.write(filtered_data)


# Menggunakan hanya kolom yang diperlukan untuk analisis
filtered_day_df = day_df[['dteday', 'season', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']]

# Menghitung jumlah sewa berdasarkan cuaca
weather_effect = filtered_day_df.groupby('weathersit')['cnt'].sum().reset_index()

# Menampilkan data
print("Pengaruh Cuaca terhadap Jumlah Sewa Sepeda:")
print(weather_effect)

# Menghitung jumlah sewa berdasarkan hari kerja
workingday_effect = filtered_day_df.groupby('workingday')['cnt'].sum().reset_index()

# Menampilkan data
print("Pengaruh Hari Kerja dan Hari Libur terhadap Penggunaan Sepeda:")
print(workingday_effect)


# Menambahkan filter untuk cuaca dan hari kerja
weather_filter = st.selectbox("Pilih Cuaca", options=filtered_day_df['weathersit'].unique())
workingday_filter = st.selectbox("Pilih Hari Kerja", options=[0, 1])  # 0 = tidak, 1 = ya

# Menggunakan filter untuk menampilkan data yang sesuai
filtered_data = filtered_day_df[(filtered_day_df['weathersit'] == weather_filter) & (filtered_day_df['workingday'] == workingday_filter)]

st.write("Data yang Difilter:")
st.dataframe(filtered_data)


# Visualisasi Penyewaan Berdasarkan Cuaca
plt.figure(figsize=(10, 5))
sns.barplot(x='weathersit', y='cnt', data=weather_effect)
plt.title('Jumlah Penyewaan Sepeda Berdasarkan Cuaca')
plt.xlabel('Cuaca')
plt.ylabel('Jumlah Penyewaan')
plt.xticks(rotation=45)
st.pyplot(plt)  # Menampilkan plot di Streamlit

# Mengonversi kolom 'dteday' menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Mendapatkan tanggal terakhir dari dataset
last_date = day_df['dteday'].max()

# Mengonversi kolom 'dteday' menjadi datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Mendapatkan tanggal terakhir dari dataset
last_date = day_df['dteday'].max()

# Menghitung RFM
rfm = day_df.groupby('casual').agg(
    Recency=('dteday', lambda x: (last_date - x.max()).days),  # Menggunakan tuple
    Frequency=('casual', 'count'),  # Total penyewaan
    Monetary=('cnt', 'sum')  # Total penyewaan
).reset_index()

print(rfm)






