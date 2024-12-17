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
        "Top Product Categories by Sales Value",
        "Shipping Time vs Customer Satisfaction",
        "Payment Methods by Total Sales Value",
        "Monthly Sales Pattern",
        "High-Value Transactions by Payment Method",
        "Average Shipping Time by Customer Location"
    ]
    selected_analysis = st.selectbox("🔍 Select Analysis", analysis_options)

# Analysis 1: Top Product Categories by Sales Value
if selected_analysis == "Top Product Categories by Sales Value":
    category_sales_df = all_df.groupby('product_category_name').agg({
        'product_id': 'count',
        'total_value': 'sum'
    }).rename(columns={'product_id': 'total_quantity'}).sort_values(by='total_value', ascending=False).reset_index()

    # Subheader dengan HTML untuk pemusatan
    st.markdown("""
        <h2 style='text-align: center; color: #FFA500;'>🏆 Top Product Categories by Sales Value</h2>
    """, unsafe_allow_html=True)
    
    # Tampilkan dataframe
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:  # Dataframe berada di kolom tengah
        st.dataframe(category_sales_df)

    # Ambil 10 kategori teratas berdasarkan total sales value
    top_10_category_sales_df = category_sales_df.head(10)

    # Visualisasi dengan barplot
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="total_value", y="product_category_name", data=top_10_category_sales_df, color='lightgreen', ax=ax)
    ax.set_title("Top 10 Product Categories by Sales Value", fontsize=16)
    ax.set_xlabel("Total Sales Value", fontsize=12)
    ax.set_ylabel("Product Category", fontsize=12)
    st.pyplot(fig)

    st.markdown("""
    <h3 style='text-align: left;'>💡 INSIGHT</h3>
    <p style='font-family: Roboto, sans-serif; text-align: justify; color: #FFFFFF; font-size: 14px'>Secara keseluruhan, visualisasi ini menunjukkan bahwa kategori produk tertentu memiliki kontribusi dominan terhadap nilai penjualan. Kategori seperti <strong>"beleza_saude", "relogios_presentes", dan "cama_mesa_banho"</strong> menempati posisi teratas, mencerminkan tingginya permintaan untuk produk-produk tersebut. Sementara itu, kategori lainnya memiliki kontribusi lebih rendah. Insight ini dapat membantu dalam pengambilan keputusan terkait strategi pemasaran, pengelolaan stok, dan fokus bisnis pada kategori dengan performa terbaik untuk memaksimalkan pendapatan.</p>
    """, unsafe_allow_html=True)

# Analysis 2: Shipping Time vs Customer Satisfaction
elif selected_analysis == "Shipping Time vs Customer Satisfaction":
    # Konversi kolom menjadi datetime
    all_df['review_creation_date'] = pd.to_datetime(all_df['review_creation_date'], errors='coerce')
    all_df['shipping_limit_date'] = pd.to_datetime(all_df['shipping_limit_date'], errors='coerce')
    # Hitung shipping_time
    all_df['shipping_time'] = (all_df['review_creation_date'] - all_df['shipping_limit_date']).dt.days
    # Hapus baris dengan nilai NaT
    all_df = all_df.dropna(subset=['review_creation_date', 'shipping_limit_date'])

    # Analisis Shipping Time vs Review Score
    shipping_review_df = all_df.groupby('shipping_time')['review_score'].mean().reset_index()
    # Filter shipping_time
    shipping_review_df = shipping_review_df.query('-50 <= shipping_time <= 50')

    # Subheader dengan HTML untuk pemusatan
    st.markdown("""
        <h2 style='text-align: center; color: #FFA500;'>🚚 Shipping Time vs Customer Satisfaction</h2>
    """, unsafe_allow_html=True)

    # Tampilkan dataframe
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:  # Dataframe berada di kolom tengah
        st.dataframe(shipping_review_df)

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.scatterplot(x="shipping_time", y="review_score", data=shipping_review_df, color='coral', s=50, ax=ax)
    sns.lineplot(x="shipping_time", y="review_score", data=shipping_review_df, color='teal', ax=ax)
    ax.set_title("Shipping Time vs Customer Satisfaction (Review Score)", fontsize=16)
    ax.set_xlabel("Shipping Time (Days)", fontsize=12)
    ax.set_ylabel("Average Review Score", fontsize=12)
    ax.axhline(y=4, color='grey', linestyle='--', linewidth=1, label='Target Review Score = 4')
    ax.legend()
    st.pyplot(fig)

    st.markdown("""
    <h3 style='text-align: left;'>💡 INSIGHT</h3>
    <p style='font-family: Roboto, sans-serif; text-align: justify; color: #FFFFFF; font-size: 14px'>Pengiriman yang <strong>cepat dan tepat waktu</strong> adalah faktor kunci dalam menjaga kepuasan pelanggan, sementara keterlambatan memiliki dampak negatif yang signifikan. Optimalisasi logistik diperlukan untuk meningkatkan performa pengiriman dan memastikan review score tetap berada di atas target.</p>
    """, unsafe_allow_html=True)

# Analysis 3: Payment Methods by Total Sales Value
elif selected_analysis == "Payment Methods by Total Sales Value":
    payment_method_df = all_df.groupby('payment_type').agg({
        'order_id': 'nunique',
        'total_value': 'sum'
    }).reset_index()

    # Subheader dengan HTML untuk pemusatan
    st.markdown("""
        <h2 style='text-align: center; color: #FFA500;'>💳 Payment Methods by Total Sales Value</h2>
    """, unsafe_allow_html=True)

    # Tampilkan dataframe
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:  # Dataframe berada di kolom tengah
        st.dataframe(payment_method_df)

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="payment_type", y="total_value", data=payment_method_df, color="red", ax=ax)
    ax.set_title("Payment Methods by Total Sales Value", fontsize=16)
    ax.set_xlabel("Payment Method", fontsize=12)
    ax.set_ylabel("Total Sales Value", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    st.markdown("""
    <h3 style='text-align: left;'>💡 INSIGHT</h3>
    <p style='font-family: Roboto, sans-serif; text-align: justify; color: #FFFFFF; font-size: 14px'>Penggunaan <strong>credit_card</strong> sebagai metode pembayaran utama menunjukkan preferensi pelanggan terhadap metode ini. Strategi bisnis dapat difokuskan pada promosi dan peningkatan layanan terkait pembayaran dengan kartu kredit untuk mendorong penjualan lebih lanjut.</p>
    """, unsafe_allow_html=True)

# Analysis 4: Monthly Sales Pattern
elif selected_analysis == "Monthly Sales Pattern":
    all_df['order_date'] = pd.to_datetime(all_df['order_purchase_timestamp'])
    all_df['order_month'] = all_df['order_date'].dt.month

    monthly_sales_df = all_df.groupby('order_month').agg({
        'order_id': 'nunique',
        'total_value': 'sum'
    }).reset_index()

    # Subheader dengan HTML untuk pemusatan
    st.markdown("""
        <h2 style='text-align: center; color: #FFA500;'>📅 Monthly Sales Pattern</h2>
    """, unsafe_allow_html=True)
    
    # Tampilkan dataframe
    col1, col2, col3 = st.columns([1, 1.6, 1])
    with col2:  # Dataframe berada di kolom tengah
        st.dataframe(monthly_sales_df)

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x="order_month", y="total_value", data=monthly_sales_df, marker='o', color='orange', ax=ax)
    ax.set_title("Monthly Sales Pattern", fontsize=16)
    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Total Sales Value", fontsize=12)
    ax.set_xticks(range(12))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    st.pyplot(fig)

    st.markdown("""
    <h3 style='text-align: left;'>💡 INSIGHT</h3>
    <p style='font-family: Roboto, sans-serif; text-align: justify; color: #FFFFFF; font-size: 14px'>Visualisasi <strong>Monthly Sales Pattern</strong> menunjukkan pola fluktuasi penjualan sepanjang tahun. Penjualan mencapai puncaknya pada bulan <strong>Juni</strong> dan tetap tinggi di <strong>Agustus</strong>, sementara penurunan tajam terlihat di bulan <strong>September</strong> dan <strong>Oktober</strong>, dengan pemulihan kecil di bulan <strong>November</strong>. Tren ini dapat mencerminkan periode musiman atau momen khusus yang memengaruhi aktivitas penjualan, seperti promosi, hari libur, atau faktor eksternal lainnya. Perusahaan dapat merencanakan strategi promosi dan stok yang lebih efektif pada bulan dengan penjualan tinggi serta mengidentifikasi penyebab penurunan untuk memaksimalkan potensi penjualan.</p>
    """, unsafe_allow_html=True)
    
# Analysis 5: High-Value Transactions by Payment Method
elif selected_analysis == "High-Value Transactions by Payment Method":
    high_value_transactions_df = all_df.sort_values(by='total_value', ascending=False).head(100)
    payment_method_high_value_df = high_value_transactions_df.groupby('payment_type').agg({
        'order_id': 'nunique',
        'total_value': 'sum'
    }).reset_index()

    # Subheader dengan HTML untuk pemusatan
    st.markdown("""
        <h2 style='text-align: center; color: #FFA500; font-size: 32px'>💎 High-Value Transactions by Payment Method</h2>
    """, unsafe_allow_html=True)

    # Tampilkan dataframe
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:  # Dataframe berada di kolom tengah
        st.dataframe(payment_method_high_value_df)

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="payment_type", y="total_value", data=payment_method_high_value_df, color='skyblue', ax=ax)
    ax.set_title("Payment Methods for High-Value Transactions", fontsize=16)
    ax.set_xlabel("Payment Method", fontsize=12)
    ax.set_ylabel("Total Sales Value", fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    st.markdown("""
    <h3 style='text-align: left;'>💡 INSIGHT</h3>
    <p style='font-family: Roboto, sans-serif; text-align: justify; color: #FFFFFF; font-size: 14px'>Visualisasi <strong>High-Value Transactions by Payment Method</strong> menunjukkan bahwa metode <strong>credit card</strong> mendominasi transaksi dengan nilai tinggi, baik dari segi jumlah transaksi (82 order) maupun total nilai penjualan (191,418.95). Sementara itu, metode boleto berada di posisi kedua, diikuti oleh <strong>debit card</strong> dan <strong>voucher</strong>, yang memiliki kontribusi paling kecil. Metode pembayaran <strong>credit card</strong> sangat efektif untuk mendorong transaksi bernilai tinggi, sehingga perusahaan dapat mempertimbangkan promosi atau program insentif berbasis kartu kredit untuk menarik lebih banyak pelanggan dan meningkatkan penjualan.</p>
    """, unsafe_allow_html=True)

# Analysis 6: Average Shipping Time by Customer Location
elif selected_analysis == "Average Shipping Time by Customer Location":
    # Pastikan shipping_time sudah dihitung sebelumnya
    if 'shipping_time' not in all_df.columns:
        # Konversi kolom menjadi datetime jika belum dilakukan
        all_df['review_creation_date'] = pd.to_datetime(all_df['review_creation_date'], errors='coerce')
        all_df['shipping_limit_date'] = pd.to_datetime(all_df['shipping_limit_date'], errors='coerce')
        
        # Hapus baris dengan nilai NaT
        all_df = all_df.dropna(subset=['review_creation_date', 'shipping_limit_date'])
        
        # Hitung shipping_time
        all_df['shipping_time'] = (all_df['review_creation_date'] - all_df['shipping_limit_date']).dt.days

    # Grouping by customer location
    shipping_location_df = all_df.groupby('customer_city').agg({
        'shipping_time': 'mean'
    }).reset_index()

    # Sorting descending by shipping_time
    shipping_location_df = shipping_location_df.sort_values(by='shipping_time', ascending=False)

    # Ambil 10 kota teratas
    top_cities = shipping_location_df.head(10)

    # Subheader dengan HTML untuk pemusatan
    st.markdown("""
        <h2 style='text-align: center; color: #FFA500; font-size: 32px;'>📍 Average Shipping Time by Customer Location</h2>
    """, unsafe_allow_html=True)

    # Tampilkan dataframe
    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:  # Dataframe berada di kolom tengah
        st.dataframe(shipping_location_df)

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 8))
    # Plot horizontal barplot
    sns.barplot(x="shipping_time", y="customer_city", data=top_cities, palette="Blues_r", ax=ax)
    # Tambahkan label di ujung bar
    for i, value in enumerate(top_cities['shipping_time']):
        ax.text(value + 0.5, i, f"{value:.2f}", va='center', fontsize=10)
    ax.set_title("Top 10 Cities with Highest Average Shipping Time", fontsize=16)
    ax.set_xlabel("Average Shipping Time (Days)", fontsize=12)
    ax.set_ylabel("Customer City", fontsize=12)
    st.pyplot(fig)

    st.markdown("""
    <h3 style='text-align: left;'>💡 INSIGHT</h3>
    <p style='font-family: Roboto, sans-serif; text-align: justify; color: #FFFFFF; font-size: 14px'>Visualisasi <strong>Average Shipping Time by Customer Location</strong> menunjukkan bahwa kota-kota seperti <strong>Cacimbinhas, Sao Joao do Itaperiu, dan Itacoatiara</strong> memiliki rata-rata waktu pengiriman tertinggi, dengan waktu mencapai lebih dari 30 hari. Hal ini dapat mengindikasikan adanya tantangan logistik atau jarak pengiriman yang jauh di kota-kota tersebut. Perusahaan perlu mengevaluasi dan mengoptimalkan proses pengiriman, terutama ke kota-kota dengan rata-rata waktu pengiriman tertinggi, untuk meningkatkan kepuasan pelanggan dan memastikan layanan lebih efisien.</p>
    """, unsafe_allow_html=True)

# Footer
st.markdown(
    "<p class='footer'>© 2024 Your Name | All Rights Reserved</p>",
    unsafe_allow_html=True
)