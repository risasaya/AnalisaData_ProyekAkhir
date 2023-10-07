import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
def create_daily_orders_df(df):
    df['dteday'] = pd.to_datetime(df['dteday'])
    orders_df = df.resample('M', on='dteday').sum()
    return orders_df
def create_ren_cas_df(df):
    ren_cas_df = df.groupby("weekday").casual.sum().sort_values(ascending=False).reset_index()
    return ren_cas_df
def create_ren_reg_df(df):
    ren_reg_df = df.groupby("weekday").registered.sum().sort_values(ascending=False).reset_index()
    return ren_reg_df
def create_bymonth_df(df):
    bymonth_df = df.groupby("month").Total.sum().sort_values(ascending=False).reset_index()
    return bymonth_df
def create_byweather_df(df):
    byweather_df = df.groupby("weather_situation").Total.sum().sort_values(ascending=False).reset_index()
    return byweather_df
def create_rfm(df):
    rfm_df = df.groupby(by="hour", as_index=False).agg({
    "dteday": "max", 
    "instant": "nunique", 
    "Total": "sum" 
    })
    rfm_df.columns = ["hour", "max_order_timestamp", "frequency", "monetary"]
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["dteday"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
 
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    return rfm_df

hour_df = pd.read_csv("hour_data.csv")
datetime_columns = ["dteday"]
hour_df.sort_values(by="dteday", inplace=True)
hour_df.reset_index(inplace=True)
 
for column in datetime_columns:
    hour_df[column] = pd.to_datetime(hour_df[column])

min_date = hour_df["dteday"].min()
max_date = hour_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("bike-share.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
ren_cas_df = create_ren_cas_df(main_df)
ren_reg_df = create_ren_reg_df(main_df)
bymonth_df = create_bymonth_df(main_df)
byweather_df = create_byweather_df(main_df)
rfm_df = create_rfm(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Daily Rental')
col1, col2, col3 = st.columns(3)
with col1:
    total_casual = daily_orders_df.casual.sum()
    st.metric("Total Casual Rental", value=f'{total_casual:,}')

with col2:
    total_registered = daily_orders_df.registered.sum()
    st.metric("Total Registered Rental", value=f'{total_registered:,}')
 
with col3:
    total_revenue = daily_orders_df.Total.sum()
    st.metric("Total Rental", value=f'{total_revenue:,}')

plt.figure(figsize=(10, 6))
plt.plot(daily_orders_df.index, daily_orders_df['Total'], color='#A5C0DD')
plt.xlabel(None)
plt.ylabel(None)
plt.title('Number of Rental Over Time')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

st.subheader("Performing Casual and Registered Rental by Day")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
 
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
sns.barplot(x="casual", y="weekday", data=ren_cas_df, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Casual", fontsize=30)
ax[0].set_title("Performing Casual Rental by Day", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=35)
ax[0].tick_params(axis ='x', labelsize=30)
 
sns.barplot(x="registered", y="weekday", data=ren_reg_df, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Registered", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Performing Registered Rental by Day", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

st.subheader("Number of Rental")
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(35, 15))
 
    sns.barplot(
        y="Total", 
        x="month",
        data=bymonth_df.sort_values(by="month", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Rental by Month", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35, rotation=45)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(35, 15))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="Total", 
        x="weather_situation",
        data=byweather_df.sort_values(by="weather_situation", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Rental by Weather Situation", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

st.subheader("Best Rental Based on RFM Parameters Hour")
col1, col2, col3 = st.columns(3)
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
 
colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]
 
sns.barplot(y="recency", x="hour", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hour", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=30)
ax[0].tick_params(axis ='x', labelsize=35)
 
sns.barplot(y="frequency", x="hour", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hour", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis ='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="monetary", x="hour", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("Hour", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis ='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
 
st.pyplot(fig)

copyright = f"Copyright © 2023 All Rights Reserved [Nafiatul Risa](https://www.linkedin.com/in/nafiatul-risa/)"
st.caption(copyright)
