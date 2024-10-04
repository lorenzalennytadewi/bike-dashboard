import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and preprocess the data
@st.cache_data
def load_data():
    data = pd.read_csv('dashboard/main_data.csv')
    # Select and rename relevant columns
    data = data[['dteday', 'season_x', 'registered_x', 'casual_x', 'cnt_x']].rename(columns={
        'season_x': 'season',
        'registered_x': 'registered',
        'casual_x': 'casual',
        'cnt_x': 'cnt'
    })
    data['dteday'] = pd.to_datetime(data['dteday'])
    return data

main_data = load_data()

# Title of the application
st.title('Dashboard Penyewaan Sepeda')

# Sidebar filters
st.sidebar.header("Filter Data")

# Filter by date
start_date = st.sidebar.date_input('Start date', main_data['dteday'].min())
end_date = st.sidebar.date_input('End date', main_data['dteday'].max())

# Filter by season
season_filter = st.sidebar.multiselect(
    "Pilih Musim",
    options=main_data['season'].unique(),
    default=main_data['season'].unique()
)

# Filter by user type
user_type = st.sidebar.radio(
    "Pilih Jenis Pengguna",
    ('Semua Pengguna', 'Pengguna Terdaftar', 'Pengguna Kasual')
)

# Apply filters
filtered_data = main_data[
    (main_data['dteday'] >= pd.to_datetime(start_date)) &
    (main_data['dteday'] <= pd.to_datetime(end_date)) &
    (main_data['season'].isin(season_filter))
]

if user_type == 'Pengguna Terdaftar':
    filtered_data = filtered_data[['dteday', 'registered']].copy()
    filtered_data['cnt'] = filtered_data['registered']
elif user_type == 'Pengguna Kasual':
    filtered_data = filtered_data[['dteday', 'casual']].copy()
    filtered_data['cnt'] = filtered_data['casual']

# Display filtered data preview
st.write("Data Penyewaan Sepeda", filtered_data.head())

# Plot total rental trends
st.subheader('Tren Total Penyewaan Sepeda Sepanjang Waktu')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='dteday', y='cnt', data=filtered_data, ax=ax)
plt.title('Tren Total Penyewaan Sepeda Sepanjang Waktu')
plt.xlabel('Tanggal')
plt.ylabel('Total Penyewaan Sepeda')
plt.xticks(rotation=45)
st.pyplot(fig)

# Plot rental distribution by season
st.subheader('Distribusi Penyewaan Sepeda Berdasarkan Musim')
fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(x='season', y='cnt', data=main_data[main_data['season'].isin(season_filter)], ax=ax)
plt.title('Distribusi Penyewaan Sepeda Berdasarkan Musim')
plt.xlabel('Musim')
plt.ylabel('Total Penyewaan Sepeda')
st.pyplot(fig)

# Pie chart for user type proportions
st.subheader('Proporsi Penyewaan Sepeda: Pengguna Terdaftar vs Kasual')
total_registered = main_data['registered'].sum()
total_casual = main_data['casual'].sum()

# Data for pie chart
labels = ['Pengguna Terdaftar', 'Pengguna Kasual']
sizes = [total_registered, total_casual]
colors = ['#66b3ff', '#99ff99']

# Create pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, explode=(0, 0.1))
plt.title('Proporsi Penyewaan Sepeda: Pengguna Terdaftar vs Kasual')
plt.axis('equal')
st.pyplot(fig)

# Descriptive statistics
st.subheader('Statistik Deskriptif Penyewaan Sepeda')
st.write(filtered_data.describe())

# Footer
st.markdown('**Created by Lorenza Lennyta Dewi**')
