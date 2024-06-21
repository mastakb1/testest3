import plotly.express as px

def plot_line_chart(data, color='blue'):
    fig = px.line(data, x=data.index, y='LineTotal', title='Tren Penjualan', color_discrete_sequence=[color])
    return fig

def plot_scatter_plot(data, color='blue'):
    fig = px.scatter(data, x='OrderQty', y='LineTotal', title='Relasi Antara Order Quantity dan Total Penjualan', color_discrete_sequence=[color])
    return fig

def plot_pie_chart(data):
    fig = px.pie(data, values='LineTotal', names='category', title='Kontribusi Kategori dalam Penjualan')
    return fig

def plot_histogram(data, color='blue'):
    fig = px.histogram(data, title='Distribusi Jumlah Penjualan', color_discrete_sequence=[color])
    return fig
