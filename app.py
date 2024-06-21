import streamlit as st
import pandas as pd
import plotly.express as px
from awDb import get_data_from_db

# Mendapatkan data dari tabel baru
sales_fact_df = get_data_from_db("""
    SELECT 
        fis.OrderDateKey AS time_key, 
        fis.ProductKey AS product_key, 
        fis.SalesAmount AS LineTotal, 
        fis.OrderQuantity AS OrderQty,
        fis.UnitPrice, 
        dt.FullDateAlternateKey AS fulldates,
        dt.CalendarYear AS years
    FROM 
        factinternetsales fis
    JOIN 
        dimtime dt ON fis.OrderDateKey = dt.TimeKey
""")
product_fact_df = get_data_from_db("""
    SELECT 
        dp.ProductKey AS id, 
        dp.EnglishProductName AS name, 
        dpc.EnglishProductCategoryName AS category 
    FROM 
        dimproduct dp
    JOIN 
        dimproductsubcategory dps ON dp.ProductSubcategoryKey = dps.ProductSubcategoryKey
    JOIN 
        dimproductcategory dpc ON dps.ProductCategoryKey = dpc.ProductCategoryKey
""")

# Konversi kolom tanggal
sales_fact_df['fulldates'] = pd.to_datetime(sales_fact_df['fulldates'])

# Sidebar options
st.sidebar.header('Options')
color_palette = st.sidebar.selectbox('Select Color Palette', ['plotly', 'ggplot2', 'seaborn'])

# Memilih tahun
selected_year = st.sidebar.selectbox('Select Year', sales_fact_df['years'].unique())

# Filter data berdasarkan tahun yang dipilih
filtered_sales_fact_df = sales_fact_df[sales_fact_df['years'] == selected_year]

# Data untuk plot tren penjualan harian
sales_time_df = filtered_sales_fact_df.copy()

# Gabungkan data penjualan dengan data produk
sales_product_df = pd.merge(filtered_sales_fact_df, product_fact_df, left_on='product_key', right_on='id')

# Data untuk plot pie kontribusi kategori
category_sales_df = sales_product_df.groupby('category').agg({'LineTotal': 'sum'}).reset_index()

# Data untuk histogram distribusi penjualan
sales_time_hist_df = sales_time_df['LineTotal']

# Judul utama dashboard
st.title('Sales Dashboard')

# Plot Tren Penjualan Harian
st.header('Tren Penjualan Harian')
daily_sales = sales_time_df.groupby('fulldates').agg({'LineTotal': 'sum'}).reset_index()
line_fig = px.line(daily_sales, x='fulldates', y='LineTotal', title='Tren Penjualan Harian', template=color_palette)
st.plotly_chart(line_fig)
st.write("Grafik ini menunjukkan bagaimana penjualan berubah setiap harinya sepanjang tahun yang dipilih. Pola ini dapat membantu mengidentifikasi tren musiman atau hari-hari dengan penjualan tertinggi.")
st.write("Kesimpulan: Dari tahun ke tahun, penjualan mengalami naik turun, di awal tahun trend penjualan nya adalah naik, namun cenderung tidak signifikan. namun di tahun 2002 mengalami penjualan menurun, namun setelah itu malah terjadi lonjakan penjualan di tahun 2003 dan tahun selanjutnya memberikan gambaran tren penjualan yang naik")

# Top 10 Produk Terlaris
st.header('Top 10 Produk Terlaris')
top_products = sales_product_df.groupby('name').agg({'LineTotal': 'sum'}).nlargest(10, 'LineTotal').reset_index()
for index, row in top_products.iterrows():
    progress_percent = row['LineTotal'] / top_products['LineTotal'].max()
    st.write(f"{row['name']} - Total Penjualan: {row['LineTotal']}")
    st.progress(progress_percent)
st.write("Bagian ini menampilkan produk-produk dengan total penjualan tertinggi sepanjang tahun yang dipilih. Ini membantu mengidentifikasi produk-produk yang paling populer di kalangan pelanggan.")

# Plot scatter relasi antara Order Quantity dan Total Penjualan
st.header('Relasi Antara Unit Price dan Sales Amount')
scatter_fig = px.scatter(sales_product_df, x='UnitPrice', y='LineTotal', color='category', title='Relasi Antara Unit Price dan Sales Amount', template=color_palette)
st.plotly_chart(scatter_fig)
st.write("Scatter plot ini menunjukkan hubungan antara harga unit produk dan total penjualannya. Setiap titik mewakili satu produk, dengan warna yang berbeda untuk setiap kategori produk.")
st.write("Kesimpulan : Hubungan ini menunjukan bahwa meskipun harga barang tinggi, tidak ada pengaruh nya dengan penjualan. Karena mungkin barang utama yang dijual adalah sepeda maka, meskipun harganya tinggi tetap saja penjualan tetap tinggi karena telah menemukan customer dengan niche yang pas")

# Plot pie kontribusi kategori dalam penjualan
st.header('Kontribusi Kategori dalam Penjualan')
pie_fig = px.pie(category_sales_df, values='LineTotal', names='category', title='Kontribusi Kategori dalam Penjualan', template=color_palette)
st.plotly_chart(pie_fig)
st.write("Diagram pie ini menunjukkan kontribusi masing-masing kategori produk terhadap total penjualan. Ini membantu memahami seberapa besar setiap kategori produk menyumbang terhadap pendapatan keseluruhan.")
st.write(f"Kesimpulan : dari tahun 2001 - 2002 barang yang dijual hanyalah sepedah. bisa ditunjukan dari diagram pie yang 100% adalah sepedah. Dan mulai masuk barang dari kategori baru di tahun berikut nya, tetap saja yang berkontribusi banyak adalah barang dari kategori sepeda")

# Plot histogram distribusi jumlah penjualan
st.header('Distribusi Jumlah Penjualan')
hist_fig = px.histogram(sales_time_hist_df, title='Distribusi Jumlah Penjualan', template=color_palette)
st.plotly_chart(hist_fig)
st.write("Histogram ini menunjukkan distribusi jumlah penjualan. Ini membantu memahami variasi dalam jumlah penjualan dan mengidentifikasi rentang jumlah penjualan yang paling umum.")
st.write("Kesimpulan: di tahun 2001, malah cenderung banyak penjualan dengan value tinggi. tahun 2002 mulai tersebar, namun masih banyak penjualan dari barang yang memiliki value tinggi.Namun di tahun tahun berikut nya, malah banyak penjualan dari barang bervalue rendah, mungkin dikarenakan toko tersebut mulai memasukan barang dengan harga murah dan barang dari kategori lain yang dianggap murah juga sebagai respon turun nya trend penjualan di tahun 2002")
