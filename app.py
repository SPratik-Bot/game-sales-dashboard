import streamlit as st		#Impeot the Streamlit library
import pandas as pd		#Python library for data manipulation
import plotly.express as px     #Interactive plots and visualisation library

# Page Configuration
st.set_page_config(page_title="Game Sales Dashboard", layout="wide")

# Load the dataset
@st.cache_data
def load_data():
	file_path = r"vgsales.csv"
	df = pd.read_csv(file_path)
	return df

df = load_data()


# ----------------------------- SIDEBAR FILTERS ----------------------------- #
st.sidebar.title("🎮 Game Sales Filter")
st.sidebar.markdown("Use the filters below to customize the dashboard view:")

year = st.sidebar.selectbox("📆 Release Year", sorted(df['Year'].dropna().unique()), index=0)
genre = st.sidebar.multiselect("🧩 Genre(s)", df['Genre'].unique(), default=df['Genre'].unique())
platform = st.sidebar.multiselect("🕹️ Platform(s)", df['Platform'].unique(), default=df['Platform'].unique())

# Apply filters
filtered_df = df[
    (df['Year'] == year) &
    (df['Genre'].isin(genre)) &
    (df['Platform'].isin(platform))
]

# ----------------------------- TITLE + INTRO ----------------------------- #
st.title("🎮 Game Sales Analysis Dashboard")
st.markdown("""
Welcome to the interactive dashboard built using **Streamlit** and **Plotly**.
Use the sidebar to explore video game sales data across platforms, genres, and regions.
""")

# ----------------------------- METRICS ----------------------------- #
if not filtered_df.empty:
	total_sales = filtered_df['Global_Sales'].sum()
	top_game = filtered_df.sort_values(by='Global_Sales', ascending=False).iloc[0]['Name']
	total_games = filtered_df['Name'].nunique()
else:
	total_sales = 0
	top_game = "No Data"
	total_games = 0

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Global Sales (M)", f"{total_sales:.2f}")
col2.metric("🏆 Top Game", top_game)
col3.metric("🎮 Total Games", total_games)

# ----------------------------- GENRE SALES ----------------------------- #
st.markdown("---")
st.subheader("📊 Global Sales by Genre")
genre_sales = filtered_df.groupby('Genre')['Global_Sales'].sum().reset_index()
fig1 = px.bar(genre_sales, x='Genre', y='Global_Sales', color='Genre',
              title="Sales by Genre", labels={'Global_Sales': 'Global Sales (M)'})
st.plotly_chart(fig1, use_container_width=True)

# ----------------------------- TOP 10 GAMES ----------------------------- #
st.markdown("---")
st.subheader("🏆 Top 10 Games by Global Sales")
top_games = filtered_df.sort_values(by='Global_Sales', ascending=False).head(10)
st.dataframe(top_games[['Name', 'Platform', 'Year', 'Genre', 'Global_Sales']])

# ----------------------------- REGIONAL SALES PIE ----------------------------- #
st.markdown("---")
st.subheader("🌍 Regional Sales Distribution")
region_sales = filtered_df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum().reset_index()
region_sales.columns = ['Region', 'Sales']
fig2 = px.pie(region_sales, names='Region', values='Sales',
              title="Sales Distribution by Region", hole=0.4,
              color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------- PLATFORM SALES ----------------------------- #
st.markdown("---")
st.subheader("🕹️ Global Sales by Platform")
platform_sales = filtered_df.groupby('Platform')['Global_Sales'].sum().reset_index()
platform_sales = platform_sales.sort_values(by='Global_Sales', ascending=False)
fig3 = px.bar(platform_sales, x='Platform', y='Global_Sales',
              title='Platform-wise Global Sales',
              labels={'Global_Sales': 'Global Sales (M)'},
              color='Platform', text_auto='.2s')
st.plotly_chart(fig3, use_container_width=True)

# ----------------------------- SALES TREND ----------------------------- #
st.markdown("---")
st.subheader("📅 Global Sales Trend Over the Years")
sales_trend_df = df[
    (df['Genre'].isin(genre)) &
    (df['Platform'].isin(platform))
]
sales_by_year = sales_trend_df.groupby('Year')['Global_Sales'].sum().reset_index()
sales_by_year = sales_by_year.sort_values('Year')
fig4 = px.line(sales_by_year, x='Year', y='Global_Sales',
               title='Total Global Sales Over the Years',
               markers=True,
               labels={'Global_Sales': 'Global Sales (M)', 'Year': 'Release Year'})
st.plotly_chart(fig4, use_container_width=True)

# ----------------------------- DOWNLOAD DATA ----------------------------- #
st.markdown("---")
st.subheader("💾 Download Dataset")

download_full = st.toggle("📦 Download full dataset")

# Choose which dataset to convert
data_to_download = df if download_full else filtered_df

# Convert to CSV
csv = data_to_download.to_csv(index=False).encode('utf-8')

# Download button
download_label = "📥 Download Full Dataset" if download_full else "📥 Download Filtered Dataset"
filename = 'full_game_sales.csv' if download_full else 'filtered_game_sales.csv'

st.download_button(
    label=download_label,
    data=csv,
    file_name=filename,
    mime='text/csv'
)

# ----------------------------- FOOTER ----------------------------- #
st.markdown("---")
st.markdown("Built with ❤️ by **Pratik Sawant** | Powered by Streamlit & Plotly", unsafe_allow_html=True)
