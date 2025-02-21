import pandas as pd 
import plotly_express as px
import streamlit as st

st.set_page_config(page_title="Sales Dahboard",
                   page_icon=":bar_chart:",
                   layout='wide'
)

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )

    # hour column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# sidebar

st.sidebar.header("Please filter here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)


st.sidebar.header("Please filter here:")
customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)


st.sidebar.header("Please filter here:")
gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)


df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)


# main page

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

#  top kpis

total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sales_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales per Transaction:")
    st.subheader(f"US $ {average_sales_by_transaction}")

st.markdown("---")    

# sales by product line (Bar Chart)
if "Product line" in df_selection.columns:
    # Ensure 'Total' column is numeric
    df_selection["Total"] = pd.to_numeric(df_selection["Total"], errors='coerce')
    
    # Check for NaN values after conversion
    if df_selection["Total"].isnull().any():
        st.warning("Some values in the 'Total' column could not be converted to numeric and will be ignored.")

    sales_by_product_line = (
        df_selection.groupby(by=["Product line"]).sum(numeric_only=True)[["Total"]].sort_values(by="Total")
    )
    fig_product_sales = px.bar(
        sales_by_product_line,
        x="Total",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>Sales by Product Line</b>",
        color_discrete_sequence=["#E1A140"] * len(sales_by_product_line),
        template="plotly_white",
    )

    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False)),
    )
else:
    st.error("The 'Product line' column is not available in the selected data.")

# sales by hour (bar chart)
sales_by_hour = df_selection.groupby(by=["hour"]).sum(numeric_only=True)

if "Total" in sales_by_hour.columns:
    fig_hourly_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="Total",
        title="<b>Sales by hour</b>",
        color_discrete_sequence=["#E1A140"] * len(sales_by_hour),
        template="plotly_white",
    )
    fig_hourly_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
    )
else:
    st.error("The 'Total' column is not available in the grouped data.")

# Create two columns for the charts
left_column, right_column = st.columns(2)

# Display the charts in the respective columns
if "Total" in sales_by_hour.columns:
    left_column.plotly_chart(fig_hourly_sales, use_container_width=True)

if "Total" in sales_by_product_line.columns:
    right_column.plotly_chart(fig_product_sales, use_container_width=True)

# hide steamlit style
hide_st_style= """
            <style>
            #MainMenu {visibility" hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True) 