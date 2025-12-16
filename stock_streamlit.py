import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

def get_connection():
    return psycopg2.connect(
    host="localhost",
    database="stockdb",
    user="postgres",
    password="Pavikamal29",
    port="5432"
        
    )

def load_table(table_name):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name};", conn)
    conn.close()
    df.columns = df.columns.str.strip().str.lower()
    return df


st.set_page_config(layout="wide")
st.title("📊 STOCK ANALYSIS DASHBOARD")

#MARKET SUMMARY:


st.subheader("📌 Market Summary")

summary_df = load_table("market_summary")
summary_df.columns = summary_df.columns.str.lower()

# Normalize metric names
summary_df["metric"] = summary_df["metric"].str.lower()

# ---- SAFE extraction function ----
def get_metric(summary_df, metric_name):
    row = summary_df.loc[summary_df["metric"] == metric_name, "value"]
    return row.values[0] if len(row) > 0 else None

# ---- Extract values ----
green_stocks = get_metric(summary_df, "green stocks")
red_stocks   = get_metric(summary_df, "red stocks")
avg_price    = get_metric(summary_df, "average close price")
avg_volume   = get_metric(summary_df, "average volume")   # <--- NEW

# ---- Display Metrics ----
c1, c2, c3, c4 = st.columns(4)

c1.metric("Green Stocks", int(green_stocks) if green_stocks else "NA")
c2.metric("Red Stocks", int(red_stocks) if red_stocks else "NA")
c3.metric("Avg Price", f"{avg_price:.2f}" if avg_price else "NA")
c4.metric("Avg Volume", f"{avg_volume:,.0f}" if avg_volume else "NA")


#######TOP10 GREEN STOCKS:

st.header("📈 Top 10 Yearly Returns")

st.header("🟢 Top 10 Green Stocks")

green_df = load_table("top10_green_stocks")

green_df = (
    green_df
    .groupby("ticker", as_index=False)["yearly_return"]
    .max()
    .sort_values("yearly_return", ascending=False)
    .head(10)
    .reset_index(drop=True)
)

st.dataframe(green_df)

st.header("🔴 Top 10 Loss Stocks")

loss_df = load_table("top10_loss_stocks")

loss_df = (
    loss_df
    .groupby("ticker", as_index=False)["yearly_return"]
    .min()
    .sort_values("yearly_return", ascending=True)
    .head(10)
    .reset_index(drop=True)
)

st.dataframe(loss_df)






# 1️⃣ TOP 10 VOLATILE STOCKS
# -----------------------------------------------------------
st.header("1️⃣ Top 10 Volatile Stocks")



volatile_df = load_table("top10_volatile_stocks")


volatile_df = (
    volatile_df
    .groupby("ticker", as_index=False)["volatility"]
    .max()
    .sort_values("volatility", ascending=False)
    .head(10)
    .reset_index(drop=True) 
)

st.dataframe(volatile_df)





fig, ax = plt.subplots(figsize=(10,5))

ax.bar(
    range(len(volatile_df)),
    volatile_df["volatility"]
)

ax.set_xticks(range(len(volatile_df)))
ax.set_xticklabels(volatile_df["ticker"], rotation=45)

ax.set_xlabel("Ticker")
ax.set_ylabel("Volatility")
ax.set_title("Top 10 Volatile Stocks")

st.pyplot(fig)


# 2️⃣ TOP 5 CUMULATIVE RETURN
st.header("2️⃣ Top 5 Cumulative Returns")




cum_df = load_table("top5_cumulative_return")  

cum_df = (
    cum_df
    .groupby("ticker", as_index=False)["cumulative_return"]
    .max()
    .sort_values("cumulative_return", ascending=False)
    .head(5)
    .reset_index(drop=True)   
)

st.dataframe(cum_df)


fig, ax = plt.subplots(figsize=(8,4))


ax.plot(cum_df["ticker"], cum_df["cumulative_return"], marker='o', linestyle='-', color='blue')

ax.set_xlabel("Ticker")
ax.set_ylabel("Cumulative Return")
ax.set_title("Top 5 Cumulative Returns")


ax.grid(True)

st.pyplot(fig)

####################
st.header("3️⃣ Top 5 Monthly Gainers & Losers - Horizontal Bar Chart")

gl_df = load_table("top5_gainers_losers_allmonths")
gl_df.columns = gl_df.columns.str.strip().str.lower()

gainers = gl_df[gl_df["type"].str.contains("gainer", case=False)]
losers  = gl_df[gl_df["type"].str.contains("losser", case=False)]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Gainers")
    fig, ax = plt.subplots()
    ax.barh(gainers["ticker"], gainers["return"])
    ax.set_title("Gainers")
    st.pyplot(fig)

with col2:
    st.subheader("Top Losser")
    fig, ax = plt.subplots()
    ax.barh(losers["ticker"], losers["return"])
    ax.set_title("Losser")
    st.pyplot(fig)

gl_df = load_table("top5_gainers_losers_allmonths")
gl_df.columns = gl_df.columns.str.strip().str.lower()

# Convert month to string (safe for dropdown)
gl_df["month"] = gl_df["month"].astype(str)

# Month selector
selected_month = st.selectbox(
    "📅 Select Month",
    sorted(gl_df["month"].unique())
)

# Filter selected month
month_df = gl_df[gl_df["month"] == selected_month]

gainers = month_df[month_df["type"].str.contains("gainer", case=False)]
losers  = month_df[month_df["type"].str.contains("losser", case=False)]

col1, col2 = st.columns(2)

# -------- GAINERS --------
with col1:
    st.subheader("📈 Top 5 Gainers")
    st.write(gainers)

    fig, ax = plt.subplots(figsize=(6,4))
    ax.barh(
        gainers["ticker"],
        gainers["return"],
        color="green"
    )
    ax.set_xlabel("Return")
    ax.set_title(f"Gainers - {selected_month}")
    ax.invert_yaxis()
    st.pyplot(fig)

# -------- LOSERS --------
with col2:
    st.subheader("📉 Top 5 Lossers")
    st.write(losers)

    fig, ax = plt.subplots(figsize=(6,4))
    ax.barh(
        losers["ticker"],
        losers["return"],
        color="red"
    )
    ax.set_xlabel("Return")
    ax.set_title(f"Lossers - {selected_month}")
    ax.invert_yaxis()
    st.pyplot(fig)

# 4️⃣ CORRELATION HEATMAP (WIDE FORMAT)

st.header("4️⃣ Stock Correlation Matrix - Heatmap")

corr_df = load_table("stock_correlation_matrix")
corr_df.columns = corr_df.columns.str.strip().str.lower()



corr_pivot = corr_df.pivot_table(
    index="stock1",
    columns="stock2",
    values="correlation",
    
)

fig, ax = plt.subplots(figsize=(10, 7))
im = ax.imshow(corr_pivot, cmap="coolwarm")
plt.colorbar(im)

ax.set_title("Correlation Heatmap")

ax.set_xticks(range(len(corr_pivot.columns)))
ax.set_xticklabels(corr_pivot.columns, rotation=90)

ax.set_yticks(range(len(corr_pivot.index)))
ax.set_yticklabels(corr_pivot.index)

plt.tight_layout()
st.pyplot(fig)

####

st.header("4.1) Top 10 Stock Correlation Heatmap")

corr_df = load_table("stock_correlation_matrix")
corr_df.columns = corr_df.columns.str.strip().str.lower()

corr_df["correlation"] = pd.to_numeric(
    corr_df["correlation"], errors="coerce"
)

corr_df = corr_df.dropna(subset=["stock1", "stock2", "correlation"])

corr_df["stock1"] = corr_df["stock1"].astype(str)
corr_df["stock2"] = corr_df["stock2"].astype(str)

# 🔹 Remove self-correlation for ranking
rank_df = corr_df[corr_df["stock1"] != corr_df["stock2"]]

# 🔹 Compute average absolute correlation per stock
stock_score = (
    rank_df
    .assign(abs_corr=rank_df["correlation"].abs())
    .groupby("stock1")["abs_corr"]
    .mean()
    .sort_values(ascending=False)
)

# 🔹 Select EXACT top 10 stocks
top_10_stocks = stock_score.head(10).index.tolist()

# 🔹 Filter data for those 10 stocks
filtered_corr = corr_df[
    corr_df["stock1"].isin(top_10_stocks) &
    corr_df["stock2"].isin(top_10_stocks)
]

# 🔹 Pivot to 10 × 10 matrix
corr_pivot = filtered_corr.pivot_table(
    index="stock1",
    columns="stock2",
    values="correlation",
    aggfunc="mean"
)

# 🔹 Ensure perfect 10 × 10 order
corr_pivot = corr_pivot.reindex(
    index=top_10_stocks,
    columns=top_10_stocks
)

# 🔹 Fill diagonal
for s in top_10_stocks:
    corr_pivot.loc[s, s] = 1.0

# 🔹 Plot heatmap
fig, ax = plt.subplots(figsize=(10, 7))
im = ax.imshow(corr_pivot, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(im)

ax.set_title("Top 10 Stock Correlation Heatmap")

ax.set_xticks(range(10))
ax.set_xticklabels(top_10_stocks, rotation=90)

ax.set_yticks(range(10))
ax.set_yticklabels(top_10_stocks)

plt.tight_layout()
st.pyplot(fig)




# -----------------------------------------------------------
# 5️⃣ Sector Performance (Bar Chart)
# -----------------------------------------------------------
st.header("5️⃣ Sector Performance - Bar Chart")


sector_df = load_table("sector_performance")
sector_df.columns = sector_df.columns.str.strip().str.lower()

st.write(sector_df)

sector_df["average_yearly_return"] = pd.to_numeric(
    sector_df["average_yearly_return"], errors="coerce"
)

# Drop null values if any
sector_df = sector_df.dropna(subset=["average_yearly_return"])

# Sort by highest return
sector_df = sector_df.sort_values(
    by="average_yearly_return", ascending=False
)

fig, ax = plt.subplots(figsize=(8,4))

ax.bar(sector_df["sector"], sector_df["average_yearly_return"],color='blue')
ax.set_xlabel("Sector")
ax.set_ylabel("Average Yearly Return")
ax.set_title("Sector Performance")
plt.xticks(rotation=45)

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)

sector_df = load_table("sector_performance")
sector_df.columns = sector_df.columns.str.strip().str.lower()

# Convert to numeric
sector_df["average_yearly_return"] = pd.to_numeric(
    sector_df["average_yearly_return"], errors="coerce"
)

# Drop null values
sector_df = sector_df.dropna(subset=["average_yearly_return"])

# ------------------ SECTOR DROPDOWN ------------------
selected_sector = st.selectbox(
    "Select Sector",
    sector_df["sector"].unique()
)

# Filter based on selected sector
filtered_df = sector_df[sector_df["sector"] == selected_sector]

# ------------------ BAR CHART ------------------
fig, ax = plt.subplots(figsize=(6,4))

ax.bar(
    filtered_df["sector"],
    filtered_df["average_yearly_return"]
)

ax.set_xlabel("Sector")
ax.set_ylabel("Average Yearly Return")
ax.set_title(f"Sector Performance - {selected_sector}")

plt.tight_layout()
st.pyplot(fig)

###############################
