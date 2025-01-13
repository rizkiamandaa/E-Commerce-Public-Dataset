#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import os

# CSS Styling untuk tema dark mode dan font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    .block-container {
        background-color: #1E1E1E;
        color: #F5F5F5;
        font-family: 'Roboto', sans-serif;
    }
    .stSidebar {
        background-color: #282828;
        color: #F5F5F5;
    }
    h1, h2, h3 {
        color: #FFA500;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        margin-top: 50px;
        color: #A9A9A9;
    }
    </style>
""", unsafe_allow_html=True)

# In[2]:

all_df = pd.read_csv("all_df.csv")
all_df.head()

# In[3]:

# Judul Dashboard
st.markdown(
    "<h1 style='text-align: center; color: #FAB387;'>📊 Business Analysis Dashboard</h1>",
    unsafe_allow_html=True
)

# Sidebar untuk Profil Pengguna
with st.sidebar:
    # st.image("profile.png", width=150)  # Foto profil
    st.markdown("""
        <h1 style="color:#FAB387;">👤 Profile</h3>
        <p><strong>Name:</strong> Rizki Amanda Putri</p>
        <p><strong>Role:</strong> Data Scientist</p>
        """, unsafe_allow_html=True)
    analysis_options = [
        "🛒 Top Revenue-Contributing Products and Their Share in Total Revenue",
        "💳 Distribution of Payment Methods and the Dominance of Each",
        "🌟 Impact of Customer Review Ratings on Revenue",
        "🔧 RFM Analysis"
    ]
    
    all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])
    # Urutkan data berdasarkan 'order_purchase_timestamp'
    all_df.sort_values(by='order_purchase_timestamp', inplace=True)
    all_df.reset_index(drop=True, inplace=True)
    
    # Tentukan nilai minimum dan maksimum dari kolom tanggal
    min_date = all_df['order_purchase_timestamp'].min().date()
    max_date = all_df['order_purchase_timestamp'].max().date()
    
    # Sidebar di dashboard Streamlit
    with st.sidebar:
        # Menambahkan logo perusahaan (opsional)
        # st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
        
        # Input rentang waktu dengan nilai default dari min_date ke max_date
        start_date, end_date = st.date_input(
            label='Rentang Waktu',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    
    # Filter data berdasarkan rentang tanggal
    main_df = all_df[
        (all_df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) & 
        (all_df['order_purchase_timestamp'] <= pd.Timestamp(end_date))
    ]
    
    # Tampilkan hasil filter data
    # st.write(main_df)
    
    selected_analysis = st.selectbox("🔍 Select Analysis", analysis_options)

# Analysis 1: Top Revenue-Contributing Products and Their Share in Total Revenue
if selected_analysis == "🛒 Top Revenue-Contributing Products and Their Share in Total Revenue":
    # Analisis dan visualisasi
    product_revenue_df = main_df.groupby('product_category_name').agg({
        'price': 'sum'
    }).reset_index()
    product_revenue_df.rename(columns={'price': 'total_revenue'}, inplace=True)
    top_products_df = product_revenue_df.sort_values(by='total_revenue', ascending=False)
    total_revenue = top_products_df['total_revenue'].sum()
    top_products_df['percentage_contribution'] = (top_products_df['total_revenue'] / total_revenue) * 100
    top_10_products = top_products_df.head(10)

    st.subheader("🌟 Top 10 Produk Berdasarkan Revenue")
    st.dataframe(top_10_products)

    # Bar chart
    st.subheader("📊 Kontribusi Revenue per Kategori Produk")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(top_10_products['product_category_name'], top_10_products['total_revenue'], color='skyblue')
    ax.set_xlabel("Total Revenue")
    ax.set_ylabel("Product Category")
    ax.set_title("Top 10 Product Categories by Revenue")
    ax.invert_yaxis()
    st.pyplot(fig)

    # Pie chart
    st.subheader("🥇 Persentase Kontribusi Top 10 Produk terhadap Total Revenue")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        top_10_products['total_revenue'], 
        labels=top_10_products['product_category_name'], 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=plt.cm.tab20c.colors
    )
    ax.set_title("Revenue Contribution by Top 10 Product Categories")
    st.pyplot(fig)

    # st.markdown("""
    # <h3 style='text-align: left;'>💡 INSIGHT</h3>
    # <p style='font-family: Roboto, sans-serif; text-align: justify; color: #FFFFFF; font-size: 14px'>Secara keseluruhan, visualisasi ini menunjukkan bahwa kategori produk tertentu memiliki kontribusi dominan terhadap nilai penjualan. Kategori seperti <strong>"beleza_saude", "relogios_presentes", dan "cama_mesa_banho"</strong> menempati posisi teratas, mencerminkan tingginya permintaan untuk produk-produk tersebut. Sementara itu, kategori lainnya memiliki kontribusi lebih rendah. Insight ini dapat membantu dalam pengambilan keputusan terkait strategi pemasaran, pengelolaan stok, dan fokus bisnis pada kategori dengan performa terbaik untuk memaksimalkan pendapatan.</p>
    # """, unsafe_allow_html=True)

# Analysis 2: Distribution of Payment Methods and the Dominance of Each
elif selected_analysis == "💳 Distribution of Payment Methods and the Dominance of Each":
    # Analisis dan visualisasi
    payment_distribution_df = main_df['payment_type'].value_counts().reset_index()
    payment_distribution_df.columns = ['payment_type', 'count']
    total_payments = payment_distribution_df['count'].sum()
    payment_distribution_df['percentage'] = (payment_distribution_df['count'] / total_payments) * 100

    st.subheader("💳 Distribusi Metode Pembayaran")
    st.dataframe(payment_distribution_df)

    # Pie chart
    st.subheader("📈 Distribusi Metode Pembayaran dalam Persentase")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
        payment_distribution_df['count'], 
        labels=payment_distribution_df['payment_type'], 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=plt.cm.Set3.colors
    )
    ax.set_title("Payment Method Distribution")
    st.pyplot(fig)

    # Bar chart
    st.subheader("🔢 Distribusi Metode Pembayaran dalam Angka")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(payment_distribution_df['payment_type'], payment_distribution_df['percentage'], color='coral')
    ax.set_xlabel("Payment Method")
    ax.set_ylabel("Percentage (%)")
    ax.set_title("Payment Method Percentage Distribution")
    st.pyplot(fig)

    # st.markdown("""
    # <h3 style='text-align: left;'>💡 INSIGHT</h3>
    # <p style='font-family: Roboto, sans-serif; text-align: justify; color: #FFFFFF; font-size: 14px'>Pengiriman yang <strong>cepat dan tepat waktu</strong> adalah faktor kunci dalam menjaga kepuasan pelanggan, sementara keterlambatan memiliki dampak negatif yang signifikan. Optimalisasi logistik diperlukan untuk meningkatkan performa pengiriman dan memastikan review score tetap berada di atas target.</p>
    # """, unsafe_allow_html=True)

# Analysis 3: Impact of Customer Review Ratings on Revenue
elif selected_analysis == "🌟 Impact of Customer Review Ratings on Revenue":
    # Analisis dan visualisasi
    review_revenue_df = main_df.groupby('review_score').agg({
        'price': 'mean',
        'order_id': 'count'
    }).reset_index()
    review_revenue_df.rename(columns={'price': 'avg_revenue', 'order_id': 'total_orders'}, inplace=True)

    st.subheader("💵 Rata-rata Revenue dan Total Pesanan berdasarkan Skor Review")
    st.dataframe(review_revenue_df)

    # Line chart
    st.subheader("📉 Rata-rata Revenue berdasarkan Skor Review")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        review_revenue_df['review_score'], 
        review_revenue_df['avg_revenue'], 
        marker='o', 
        color='green', 
        label='Average Revenue'
    )
    ax.set_xlabel("Review Score")
    ax.set_ylabel("Average Revenue (Price)")
    ax.set_title("Average Revenue by Review Score")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Bar chart
    st.subheader("🛍️ Total Pesanan berdasarkan Skor Review")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        review_revenue_df['review_score'], 
        review_revenue_df['total_orders'], 
        color='purple', 
        alpha=0.7, 
        label='Total Orders'
    )
    ax.set_xlabel("Review Score")
    ax.set_ylabel("Total Orders")
    ax.set_title("Total Orders by Review Score")
    ax.legend()
    st.pyplot(fig)

    # st.markdown("""
    # <h3 style='text-align: left;'>💡 INSIGHT</h3>
    # <p style='font-family: Roboto, sans-serif; text-align: justify; color: #FFFFFF; font-size: 14px'>Penggunaan <strong>credit_card</strong> sebagai metode pembayaran utama menunjukkan preferensi pelanggan terhadap metode ini. Strategi bisnis dapat difokuskan pada promosi dan peningkatan layanan terkait pembayaran dengan kartu kredit untuk mendorong penjualan lebih lanjut.</p>
    # """, unsafe_allow_html=True)

# Analysis 4: RFM Analysis
elif selected_analysis == "🔧 RFM Analysis":
    # Analisis dan visualisasi
    main_df.rename(columns={'order_purchase_timestamp': 'order_date'}, inplace=True)
    # kolom 'order_date' dalam format datetime
    # main_df['order_date'] = pd.to_datetime(all_df['order_date'])
    rfm_df = main_df.groupby(by="customer_id", as_index=False).agg({
        "order_date": "max",
        "order_id": "nunique",
        "price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    recent_date = main_df["order_date"].max()
    rfm_df["recency"] = (recent_date - rfm_df["max_order_timestamp"]).dt.days
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    
    # Ranks dan normalisasi
    rfm_df['r_rank'] = rfm_df['recency'].rank(ascending=False)
    rfm_df['f_rank'] = rfm_df['frequency'].rank(ascending=True)
    rfm_df['m_rank'] = rfm_df['monetary'].rank(ascending=True)
    rfm_df['r_rank_norm'] = (rfm_df['r_rank'] / rfm_df['r_rank'].max()) * 100
    rfm_df['f_rank_norm'] = (rfm_df['f_rank'] / rfm_df['f_rank'].max()) * 100
    rfm_df['m_rank_norm'] = (rfm_df['m_rank'] / rfm_df['m_rank'].max()) * 100
    rfm_df.drop(columns=['r_rank', 'f_rank', 'm_rank'], inplace=True)
    
    # Hitung skor RFM
    rfm_df['RFM_score'] = 0.15 * rfm_df['r_rank_norm'] + 0.28 * rfm_df['f_rank_norm'] + 0.57 * rfm_df['m_rank_norm']
    rfm_df['RFM_score'] *= 0.05
    rfm_df = rfm_df.round(2)
    
    # Segmentasi pelanggan berdasarkan skor RFM
    rfm_df['customer_segment'] = np.where(rfm_df['RFM_score'] > 4.5, "Top customers",
                                          np.where(rfm_df['RFM_score'] > 4, "High value customer",
                                                   np.where(rfm_df['RFM_score'] > 3, "Medium value customer",
                                                            np.where(rfm_df['RFM_score'] > 1.6, 'Low value customers',
                                                                     'Lost customers'))))
    
    # Rekapitulasi segmen pelanggan
    customer_segment_df = rfm_df.groupby("customer_segment", as_index=False)['customer_id'].nunique()
    customer_segment_df.rename(columns={'customer_id': 'count'}, inplace=True)

    st.subheader("📊 RFM Metrics")
    st.dataframe(rfm_df.head(10))

    st.subheader("👥 Segmentasi Pelanggan")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=customer_segment_df, x='count', y='customer_segment', palette="muted", ax=ax)
    ax.set_title("Number of Customers in Each Segment", fontsize=15)
    ax.set_xlabel("Number of Customers")
    ax.set_ylabel("Customer Segment")
    st.pyplot(fig)

    # st.markdown("""
    # <h3 style='text-align: left;'>💡 INSIGHT</h3>
    # <p style='font-family: Roboto, sans-serif; text-align: justify; color: #FFFFFF; font-size: 14px'>Visualisasi <strong>Monthly Sales Pattern</strong> menunjukkan pola fluktuasi penjualan sepanjang tahun. Penjualan mencapai puncaknya pada bulan <strong>Juni</strong> dan tetap tinggi di <strong>Agustus</strong>, sementara penurunan tajam terlihat di bulan <strong>September</strong> dan <strong>Oktober</strong>, dengan pemulihan kecil di bulan <strong>November</strong>. Tren ini dapat mencerminkan periode musiman atau momen khusus yang memengaruhi aktivitas penjualan, seperti promosi, hari libur, atau faktor eksternal lainnya. Perusahaan dapat merencanakan strategi promosi dan stok yang lebih efektif pada bulan dengan penjualan tinggi serta mengidentifikasi penyebab penurunan untuk memaksimalkan potensi penjualan.</p>
    # """, unsafe_allow_html=True)
    
# Footer
st.markdown(
    "<p class='footer'>© 2025 Your Name | All Rights Reserved</p>",
    unsafe_allow_html=True
)