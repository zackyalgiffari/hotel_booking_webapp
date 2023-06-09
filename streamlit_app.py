import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
import pandas as pd

@st.cache_data
def load_data():
    # Load data
    df = pd.read_csv('hotel_bookings.csv')


    df['arrival_date_month'] = pd.to_datetime(df['arrival_date_month'], format='%B', errors='coerce')
    df['arrival_date_year'] = pd.to_datetime(df['arrival_date_year'], format='%Y', errors='coerce')
    df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])

    # Combine 'arrival_date_year' and 'arrival_date_month' into one column
    df['date'] = df['arrival_date_year'].dt.year.astype(str) + '-' + df['arrival_date_month'].dt.month.astype(str)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m')

    return df

@st.cache_data
def create_visualizations(df):
    # Trend over time with segmentation
    df.sort_values('date', inplace=True)
    df_grouped = df.groupby(['date', 'market_segment']).size().reset_index(name='bookings')
    fig1 = px.line(df_grouped, x='date', y='bookings', color='market_segment', title='Total Bookings per Month by Market Segment')

    # Cohort analysis
   # Cohort analysis
    df['arrival_date_year'] = df['arrival_date_year'].dt.year
    df['cohort_year'] = df.groupby('customer_type')['arrival_date_year'].transform('min')
    df['cohort_index'] = df.groupby('customer_type').cumcount() + 1
    cohort_data = df.groupby(['cohort_year', 'cohort_index'])['is_canceled'].mean().unstack(0)
    fig2 = px.imshow(cohort_data, labels=dict(x="Cohort Year", y="Cohort Index", color="Cancellation Ratio"), title='Cancellation Ratio by Cohort')


    # Multivariate analysis
    fig3 = px.scatter(df, x='lead_time', y='adr', color='is_canceled', title='Lead Time vs. Average Daily Rate')

    # Cluster analysis
    kmeans = KMeans(n_clusters=3, random_state=0).fit(df[['lead_time', 'adr']])
    df['cluster'] = kmeans.labels_
    fig4 = px.scatter(df, x='lead_time', y='adr', color='cluster', title='Customer Clusters')

    return fig1, fig2, fig3, fig4

# Streamlit app```python
st.title('Hotel Booking Analysis')

# Load data
df = load_data()

# Create visualizations
fig1, fig2, fig3, fig4 = create_visualizations(df)

st.header('Trend over Time with Segmentation')
st.plotly_chart(fig1)

st.header('Cohort Analysis')
st.plotly_chart(fig2)

st.header('Multivariate Analysis')
st.plotly_chart(fig3)

st.header('Cluster Analysis')
st.plotly_chart(fig4)