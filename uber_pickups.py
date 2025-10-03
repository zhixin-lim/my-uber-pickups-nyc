import streamlit as st
import pandas as pd
import numpy as np

# title
st.title('Uber pickups in NYC')

# Downloads some data, puts it in a Pandas dataframe, and converts the date column from text to datetime.
# Function accepts a single parameter (nrows) which specifies the number of rows that you want to load into the df
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)")

# Inspect the raw data
# Use a button to toggle data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


# Draw a histogram
st.subheader('Number of pickups by hour')
# Use NumPy to generate a histogram that breaks down pickup times binned by hour:
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# use Streamlit's st.bar_chart() method to draw this histogram.
st.bar_chart(hist_values)
# it looks like the busiest time is 17:00 (5 P.M.).

# Filter results with a slider, plot filtered results on map
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)

