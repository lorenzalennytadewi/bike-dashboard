import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca data
main_data = pd.read_csv('https://raw.githubusercontent.com/lorenzalennytadewi/bike-dashboard/refs/heads/main/dashboard/main_data.csv')

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Menggunakan kolom yang relevan (misalnya, kolom _x untuk season, registered, casual, dll.)
main_data = main_data.rename(columns={
    'season_x': 'season',
    'registered_x': 'registered',
    'casual_x': 'casual',
    'cnt_x': 'cnt'
})

# Mengubah tipe data kolom dteday menjadi datetime
main_data['dteday'] = pd.to_datetime(main_data['dteday'])

# Judul Aplikasi
st.title('Dashboard Penyewaan Sepeda')

# Sidebar untuk filter data
st.sidebar.header("Filter Data")

# Filter berdasarkan tanggal
start_date = st.sidebar.date_input('Start date', main_data['dteday'].min())
end_date = st.sidebar.date_input('End date', main_data['dteday'].max())

# Filter berdasarkan musim
season_filter = st.sidebar.multiselect(
    "Pilih Musim",
    options=main_data['season'].unique(),
    default=main_data['season'].unique()
)

# Filter berdasarkan jenis pengguna
user_type = st.sidebar.radio(
    "Pilih Jenis Pengguna",
    ('Semua Pengguna', 'Pengguna Terdaftar', 'Pengguna Kasual')
)

# Menerapkan filter
filtered_data = main_data[
    (main_data['dteday'] >= pd.to_datetime(start_date)) &
    (main_data['dteday'] <= pd.to_datetime(end_date)) &
    (main_data['season'].isin(season_filter))
]

if user_type == 'Pengguna Terdaftar':
    filtered_data = filtered_data[['dteday', 'registered', 'cnt']].copy()
    filtered_data['cnt'] = filtered_data['registered']
elif user_type == 'Pengguna Kasual':
    filtered_data = filtered_data[['dteday', 'casual', 'cnt']].copy()
    filtered_data['cnt'] = filtered_data['casual']

# Plot Tren Total Penyewaan Sepeda Sepanjang Waktu
st.subheader('Tren Total Penyewaan Sepeda Sepanjang Waktu')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='dteday', y='cnt', data=filtered_data, ax=ax)
plt.title('Tren Total Penyewaan Sepeda Sepanjang Waktu')
plt.xlabel('Tanggal')
plt.ylabel('Total Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(fig)

# Plot Distribusi Penyewaan Sepeda Berdasarkan Musim
st.subheader('Distribusi Penyewaan Sepeda Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(x='season', y='cnt', data=main_data[main_data['season'].isin(season_filter)], ax=ax)
plt.title('Distribusi Penyewaan Sepeda Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Total Penyewaan Sepeda')
st.pyplot(fig)

# Pie chart proporsi pengguna terdaftar vs kasual
st.subheader('Proporsi Penyewaan Sepeda: Pengguna Terdaftar vs Kasual')
total_registered = main_data['registered'].sum()
total_casual = main_data['casual'].sum()

# Data untuk pie chart
labels = ['Pengguna Terdaftar', 'Pengguna Kasual']
sizes = [total_registered, total_casual]
colors = ['#66b3ff', '#99ff99']

# Membuat pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, explode=(0, 0.1))
plt.title('Proporsi Penyewaan Sepeda: Pengguna Terdaftar vs Kasual')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)

# Menampilkan statistik deskriptif
st.subheader('Statistik Deskriptif Penyewaan Sepeda')
st.write(filtered_data.describe())

# Footer
st.markdown('**Created by Lorenza Lennyta Dewi**')
