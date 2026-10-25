import pandas as pd
import streamlit as st

url = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/"
    "master/csse_covid_19_data/csse_covid_19_time_series/"
    "time_series_covid19_confirmed_global.csv"
)
covid = pd.read_csv(url)

covid = covid.drop(
    columns=["Province/State", "Lat", "Long"]
)
covid = covid.groupby("Country/Region").sum()
covid_daily = covid.diff(axis=1)

st.title("COVID-19 Country Dashboard")
selected_countries = st.multiselect(
    "Select countries",
    options=covid.index.tolist(),
)
display_type = st.radio(
    "Select case counts",
    options=["Cumulative cases", "Daily new cases"]
)
if display_type == "Cumulative cases":
    data = covid
else:
    data = covid_daily

if selected_countries:
    chart_data = data.loc[selected_countries].T
    chart_data.index = pd.to_datetime(
        chart_data.index, format="%m/%d/%y"
    )
    chart_data = chart_data.sort_index()

    st.line_chart(chart_data)
else:
    st.info("Please select at least one country.")