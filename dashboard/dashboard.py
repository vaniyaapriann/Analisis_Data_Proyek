import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
hour_data = pd.read_csv('dashboard/main_data.csv')
hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
hour_data['date'] = hour_data['dteday'].dt.date
hour_data['year'] = hour_data['dteday'].dt.year

# Dashboard title
st.title('Bike Rental Analysis Dashboard')

# Sidebar for navigation
st.sidebar.title('Navigation')

# Add a year selection filter with "Both" option
years = ['Both'] + list(hour_data['year'].unique())
selected_year = st.sidebar.selectbox('Select Year', years)

# Sidebar for navigation options
option = st.sidebar.selectbox('Select Analysis', 
                              ['Jumlah Penyewa per Jam', 'Penyewa Casual vs Registered', 'Penyewaan Weekdays vs Weekend'])

# Filter data based on the selected year
if selected_year == 'Both':
    hour_data_filtered = hour_data
else:
    hour_data_filtered = hour_data[hour_data['year'] == int(selected_year)]

# Pertanyaan 1: Jumlah Penyewa per Jam Tiap Harinya
if option == 'Jumlah Penyewa per Jam':
    st.header(f'Jumlah Penyewaan Sepeda per Jam Tiap Harinya ({selected_year})')

    # Grouping data
    rentals_per_hour_by_year = hour_data_filtered.groupby(['year', 'hr'])['cnt'].sum().reset_index()

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if selected_year == 'Both':
        custom_palette = {2011: "blue", 2012: "red"}
        sns.lineplot(data=rentals_per_hour_by_year, x='hr', y='cnt', hue='year', palette=custom_palette, marker='o', style='year', dashes=False, ax=ax)
        ax.set_title('Jumlah Penyewaan Sepeda per Jam Tiap Harinya (2011 vs 2012)')
    else:
        sns.lineplot(data=rentals_per_hour_by_year, x='hr', y='cnt', marker='o', color='blue' if selected_year == '2011' else 'red', ax=ax)
        ax.set_title(f'Jumlah Penyewaan Sepeda per Jam Tiap Harinya ({selected_year})')

    ax.set_xlabel('Jam (24 jam)')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_xticks(range(24))  # Show hours from 0 to 23
    ax.legend(title='Tahun', loc='upper right') if selected_year == 'Both' else None
    ax.grid(True)

    st.pyplot(fig)

# Pertanyaan 2: Jumlah Penyewa Casual vs Registered Tiap Harinya
elif option == 'Penyewa Casual vs Registered':
    st.header(f'Jumlah Penyewaan Casual dan Registered tiap Harinya ({selected_year})')

    # Grouping data
    rentals_per_hour = hour_data_filtered.groupby('hr')[['casual', 'registered']].sum().reset_index()

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    rentals_per_hour.plot(
        x='hr', 
        kind='bar', 
        stacked=True, 
        color=['skyblue', 'orange'], 
        width=0.8, 
        ax=ax
    )
    ax.set_title(f'Jumlah Penyewaan Casual dan Registered tiap Harinya ({selected_year})')
    ax.set_xlabel('Jam (24 jam)')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_xticks(range(24))
    ax.legend(['Casual', 'Registered'], title='Tipe Penyewa', loc='upper right')
    ax.grid(axis='y')

    st.pyplot(fig)

# Pertanyaan 3: Jumlah Penyewa pada Weekdays dan Weekends
elif option == 'Penyewaan Weekdays vs Weekend':
    st.header(f'Jumlah Penyewaan pada Weekdays dan Weekends ({selected_year})')

    # Create a new column for 'weekend' (1 if weekend, 0 if weekday)
    hour_data_filtered['weekend'] = hour_data_filtered['weekday'].apply(lambda x: 1 if x in [0, 6] else 0)

    # Grouping data
    weekend_rentals = hour_data_filtered.groupby('weekend')[['casual', 'registered']].sum().reset_index()

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    weekend_rentals.plot(
        x='weekend', 
        kind='bar', 
        stacked=False, 
        color=['skyblue', 'orange'], 
        width=0.8, 
        ax=ax
    )
    ax.set_title(f'Jumlah Penyewaan pada Weekdays dan Weekends ({selected_year})')
    ax.set_xlabel('(0 = Weekday, 1 = Weekend)')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_xticks([0, 1], ['Weekday', 'Weekend'])
    ax.legend(['Casual', 'Registered'], title='Tipe Penyewa', loc='upper right')
    ax.grid(axis='y')

    st.pyplot(fig)

# Insight/Recommendation Section
st.sidebar.title("Insight & Recommendation")

# Insight untuk Pertanyaan 1: Jumlah Penyewa per Jam
if option == 'Jumlah Penyewa per Jam':
    st.sidebar.subheader('Insight: Jumlah Penyewaan per Jam')
    
    # Insight berdasarkan tahun yang dipilih
    if selected_year == 'Both':
        st.sidebar.write("""
        - **Puncak aktivitas** terlihat jelas di pagi hari sekitar pukul 7-8 dan sore hari pukul 17-18 pada kedua tahun (2011 & 2012).
        - **Peningkatan jumlah penyewaan pada 2012**, terutama selama jam sibuk, dibandingkan 2011.
        """)
    elif selected_year == '2011':
        st.sidebar.write("""
        - Pada tahun 2011, puncak aktivitas penyewaan terjadi pada pukul 7-8 pagi dan 17-18 sore.
        - Jumlah penyewaan cenderung lebih rendah di luar jam sibuk.
        """)
    elif selected_year == '2012':
        st.sidebar.write("""
        - Pada tahun 2012, peningkatan penyewaan terlihat sepanjang hari, terutama selama jam sibuk.
        - Jumlah penyewaan secara keseluruhan lebih tinggi dibandingkan tahun 2011.
        """)

# Insight untuk Pertanyaan 2: Penyewa Casual vs Registered
elif option == 'Penyewa Casual vs Registered':
    st.sidebar.subheader('Insight: Penyewaan Casual dan Registered')
    st.sidebar.write("""
    - Sebagian besar penyewaan dilakukan oleh pengguna **terdaftar (registered)**, terutama selama jam sibuk (pagi dan sore hari).
    - Pengguna **casual** lebih sedikit, tetapi lebih aktif pada akhir pekan.
    - **Pola penyewaan** kedua tipe pengguna mengikuti tren yang serupa: puncak terjadi pada jam 8 pagi dan 5-6 sore.
    """)

# Insight untuk Pertanyaan 3: Penyewaan pada Weekdays vs Weekend
elif option == 'Penyewaan Weekdays vs Weekend':
    st.sidebar.subheader('Insight: Penyewaan Weekdays dan Weekends')
    st.sidebar.write("""
    - Pada **hari kerja (weekdays)**, pengguna terdaftar mendominasi penyewaan sepeda.
    - Pada **akhir pekan (weekend)**, pengguna casual meningkat, tetapi penyewaan oleh pengguna terdaftar tetap lebih tinggi.
    - Pengguna casual cenderung lebih aktif pada akhir pekan, menunjukkan bahwa mereka mungkin menggunakan sepeda untuk aktivitas rekreasi.
    """)

# Optional: Menambahkan rekomendasi untuk promosi atau pengembangan bisnis
st.sidebar.subheader("Rekomendasi")
st.sidebar.write("""
- Promosikan layanan sepeda selama **jam sibuk** (pagi dan sore hari) untuk meningkatkan penyewaan.
- **Berikan insentif** bagi pengguna casual untuk mendaftar sebagai pengguna registered, terutama pada akhir pekan.
- Pertimbangkan untuk menawarkan diskon atau program loyalitas bagi pengguna yang menyewa sepeda pada **jam non-sibuk** atau hari kerja.
""")
