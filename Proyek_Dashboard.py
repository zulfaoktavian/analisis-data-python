import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# --- Judul Dashboard ---
st.title("📊 E-Commerce Dashboard")

# --- Load Data ---
@st.cache_data
def load_data():
    # Simulasi membaca dataset (ubah path sesuai dengan file Anda)
    customers_data = pd.read_csv("C:\ZULFAA\Semester 8\Laskar AI\Projek Analisis Data dengan Python\E-Commerce Public Dataset\customers_dataset.csv")
    sellers_data = pd.read_csv("C:\ZULFAA\Semester 8\Laskar AI\Projek Analisis Data dengan Python\E-Commerce Public Dataset\sellers_dataset.csv")
    orders_data = pd.read_csv("C:\ZULFAA\Semester 8\Laskar AI\Projek Analisis Data dengan Python\E-Commerce Public Dataset\orders_dataset.csv")
    order_items_data = pd.read_csv("C:\ZULFAA\Semester 8\Laskar AI\Projek Analisis Data dengan Python\E-Commerce Public Dataset\order_items_dataset.csv")
    order_payments_data = pd.read_csv("C:\ZULFAA\Semester 8\Laskar AI\Projek Analisis Data dengan Python\E-Commerce Public Dataset\order_payments_dataset.csv")
    order_reviews_data = pd.read_csv("C:\ZULFAA\Semester 8\Laskar AI\Projek Analisis Data dengan Python\E-Commerce Public Dataset\order_reviews_dataset.csv")
    products_data = pd.read_csv("C:\ZULFAA\Semester 8\Laskar AI\Projek Analisis Data dengan Python\E-Commerce Public Dataset\products_dataset.csv")
    product_category_name = pd.read_csv("C:\ZULFAA\Semester 8\Laskar AI\Projek Analisis Data dengan Python\E-Commerce Public Dataset\product_category_name_translation.csv")
    
    return customers_data, sellers_data, orders_data, order_items_data, order_payments_data, order_reviews_data, products_data, product_category_name

customers_data, sellers_data, orders_data, order_items_data, order_payments_data, order_reviews_data, products_data, product_category_name = load_data()

# --- Fitur Interaktif: Filter Data Pelanggan ---
st.subheader("🔍 Data Pelanggan")

# Dropdown untuk memilih negara bagian pelanggan
selected_customer_state = st.selectbox("Pilih Negara Bagian (Pelanggan):", sorted(customers_data['customer_state'].unique()))

# Filter data berdasarkan negara bagian pelanggan yang dipilih
filtered_customers = customers_data[customers_data['customer_state'] == selected_customer_state]

# --- Visualisasi: Jumlah Pelanggan per Kota dalam Negara Bagian Terpilih ---
st.subheader(f"📊 Jumlah Pelanggan di Setiap Kota dalam Negara Bagian {selected_customer_state}")

city_counts_customers = customers_data[customers_data['customer_state'] == selected_customer_state] \
    .groupby('customer_city')['customer_unique_id'].nunique().reset_index()
city_counts_customers.columns = ['customer_city', 'total_customers']
top_cities_customers = city_counts_customers.sort_values(by='total_customers', ascending=False).head(10)  # 10 Kota Teratas

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=top_cities_customers['total_customers'], y=top_cities_customers['customer_city'], palette='coolwarm', ax=ax)
ax.set_xlabel("Jumlah Pelanggan")
ax.set_ylabel("Kota")
ax.set_title(f"10 Kota dengan Jumlah Pelanggan Terbanyak di {selected_customer_state}")

st.pyplot(fig)


# --- Fitur Interaktif: Filter Data Penjual ---
st.subheader("🔍 Data Penjual")

# Dropdown untuk memilih negara bagian penjual
selected_seller_state = st.selectbox("Pilih Negara Bagian (Penjual):", sorted(sellers_data['seller_state'].unique()))

# Filter data berdasarkan negara bagian penjual yang dipilih
filtered_sellers = sellers_data[sellers_data['seller_state'] == selected_seller_state]

# --- Visualisasi: Jumlah Penjual per Kota dalam Negara Bagian Terpilih ---
st.subheader(f"📊 Jumlah Penjual di Setiap Kota dalam Negara Bagian {selected_seller_state}")

city_counts_sellers = sellers_data[sellers_data['seller_state'] == selected_seller_state] \
    .groupby('seller_city')['seller_id'].nunique().reset_index()
city_counts_sellers.columns = ['seller_city', 'total_sellers']
top_cities_sellers = city_counts_sellers.sort_values(by='total_sellers', ascending=False).head(10)  # 10 Kota Teratas

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=top_cities_sellers['total_sellers'], y=top_cities_sellers['seller_city'], palette='coolwarm', ax=ax)
ax.set_xlabel("Jumlah Penjual")
ax.set_ylabel("Kota")
ax.set_title(f"10 Kota dengan Jumlah Penjual Terbanyak di {selected_seller_state}")

st.pyplot(fig)

# --- Judul Dashboard ---
st.subheader("📦 10 Kategori Produk Paling Banyak Dipesan")

# --- Menghitung jumlah pesanan per produk ---
products_order_count = order_items_data.groupby('product_id')['order_item_id'].count().reset_index()
products_order_count.columns = ['product_id', 'total_orders']

# --- Menggabungkan dengan tabel produk untuk mendapatkan kategori ---
merged_df = products_order_count.merge(products_data[['product_id', 'product_category_name']], on='product_id', how='left')

# --- Menggabungkan dengan tabel kategori untuk mendapatkan nama dalam bahasa Inggris ---
final_df = merged_df.merge(product_category_name[['product_category_name', 'product_category_name_english']], on='product_category_name', how='left')

# --- Menghitung total pesanan per kategori ---
category_order_count = final_df.groupby('product_category_name_english')['total_orders'].sum().reset_index()

# --- Mengurutkan dari yang terbanyak dipesan ---
category_order_count = category_order_count.sort_values(by='total_orders', ascending=False)

# --- Ambil 10 kategori produk yang paling banyak dipesan ---
top_categories = category_order_count.head(10)

# --- Membuat Visualisasi ---
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=top_categories['total_orders'], y=top_categories['product_category_name_english'], palette='viridis', ax=ax)
ax.set_xlabel("Total Pesanan")
ax.set_ylabel("Kategori Produk")
ax.set_title("10 Kategori Produk Paling Banyak Dipesan")

# --- Menampilkan Visualisasi ---
st.pyplot(fig)

# --- Judul Dashboard ---
st.subheader("📅 Jumlah Pesanan dan Total Pendapatan Per Tahun")

# --- Mengekstrak tahun dari shipping_limit_date ---
order_items_data['year'] = pd.to_datetime(order_items_data['shipping_limit_date']).dt.year

# --- Menghitung jumlah order per tahun ---
order_count_by_year = order_items_data.groupby('year')['order_id'].nunique().reset_index()

# --- Mengurutkan berdasarkan jumlah order tertinggi ---
order_count_by_year = order_count_by_year.sort_values(by='order_id', ascending=False)

# --- Menghitung jumlah order dan total pendapatan per tahun ---
order_summary_by_year = order_items_data.groupby('year').agg(
    total_orders=('order_id', 'nunique'),  # Hitung jumlah pesanan unik
    total_revenue=('price', 'sum')        # Hitung total pendapatan (price)
).reset_index()

# --- Mengurutkan berdasarkan jumlah order tertinggi ---
order_summary_by_year = order_summary_by_year.sort_values(by='total_orders', ascending=False)

# --- Menampilkan DataFrame di Streamlit ---
st.dataframe(order_summary_by_year, width=700)

# --- Membuat Visualisasi ---
fig, ax1 = plt.subplots(figsize=(10, 5))

# --- Membuat Visualisasi ---
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=order_count_by_year['year'], y=order_count_by_year['order_id'], palette='magma', ax=ax)
ax.set_xlabel("Tahun")
ax.set_ylabel("Jumlah Pesanan")
ax.set_title("Jumlah Pesanan Per Tahun")

# --- Menampilkan Visualisasi ---
st.pyplot(fig)
# --- Footer ---
st.markdown("© **Dashboard ini dibuat oleh Zulfaa Dwi Oktavian.**")
