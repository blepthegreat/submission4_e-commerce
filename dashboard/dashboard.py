import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load Data
@st.cache_data
def load_data():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ""))
    data_path = os.path.join(BASE_DIR, "data")
    
    order_items = pd.read_csv(os.path.join(data_path, "order_items_dataset.csv"))
    order_payments = pd.read_csv(os.path.join(data_path, "order_payments_dataset.csv"))
    products = pd.read_csv(os.path.join(data_path, "products_dataset.csv"))
    return order_items, order_payments, products

# Load datasets
order_items, order_payments, products = load_data()

# Title
st.title("E-Commerce Data Analysis Dashboard")

# Sidebar Menu for Filters
st.sidebar.header("Filter Data")
num_categories = st.sidebar.slider("Jumlah Kategori Terlaris", 5, 20, 10)

# Filter by Category Selection
selected_category = st.sidebar.multiselect(
    "Pilih Kategori Produk",
    options=products["product_category_name"].unique(),
    default=products["product_category_name"].unique().tolist()
)

# Analisis Produk Terlaris
st.header("📦 10 Kategori Produk Terlaris")
# Filter data based on selected categories
filtered_data = order_items[order_items["product_id"].isin(products[products["product_category_name"].isin(selected_category)]["product_id"])]
product_sales = filtered_data.groupby("product_id")["order_item_id"].count().reset_index()
product_sales = product_sales.merge(products, on="product_id", how="left")
product_sales = product_sales.groupby("product_category_name")["order_item_id"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=product_sales.index[:num_categories], y=product_sales.values[:num_categories], palette='coolwarm', ax=ax)
ax.set_title("Top {} Produk Kategori Terlaris".format(num_categories), fontsize=14)
ax.set_xlabel("Kategori Produk", fontsize=12)
ax.set_ylabel("Jumlah Terjual", fontsize=12)
plt.xticks(rotation=45)
st.pyplot(fig)

# Visualisasi Pie Chart
st.header("📊 Distribusi Penjualan Kategori Produk")
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(product_sales[:num_categories], labels=product_sales.index[:num_categories], autopct='%1.1f%%', startangle=140, colors=sns.color_palette("coolwarm", num_categories))
ax.set_title("Distribusi Penjualan Berdasarkan Kategori Produk")
st.pyplot(fig)

# Analisis Metode Pembayaran
st.header("💳 Metode Pembayaran yang Paling Banyak Digunakan")
payment_counts = order_payments["payment_type"].value_counts()

# Dropdown for payment method selection
payment_method = st.sidebar.selectbox("Pilih Metode Pembayaran", payment_counts.index.tolist())

# Filter by selected payment method
payment_filtered = order_payments[order_payments["payment_type"] == payment_method]

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(x=payment_counts.index, y=payment_counts.values, palette='viridis', ax=ax)
ax.set_title(f"Metode Pembayaran: {payment_method}", fontsize=14)
ax.set_xlabel("Metode Pembayaran", fontsize=12)
ax.set_ylabel("Jumlah Transaksi", fontsize=12)
plt.xticks(rotation=45)
st.pyplot(fig)

# Show more detailed information if needed
st.write("**Detail Pembayaran:**")
st.write(payment_filtered)

st.write("\n**Kesimpulan:**")
st.write("- Kategori produk yang paling banyak dibeli adalah yang memiliki jumlah order tertinggi.")
st.write("- Metode pembayaran yang paling sering digunakan perlu mendapat perhatian lebih untuk meningkatkan pengalaman pelanggan.")
