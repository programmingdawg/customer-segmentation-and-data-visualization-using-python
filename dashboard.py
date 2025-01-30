import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Online Store Sales Dashboard", 
    page_icon=":bar_chart:",
    layout="wide")


data = pd.read_csv("D:\my projects\segmentataion\myvenv\data.csv")

# drop first column
data.drop(data.columns[0], axis=1, inplace=True)

#st.dataframe(data)

# sidebar
st.sidebar.header("Please Filter here:")
city = st.sidebar.multiselect(
    "Select the Gender:",
    options=data["Gender"].unique(),
    default=data["Gender"].unique()
)


# select age category
age_category = st.sidebar.multiselect(
    "Select the Age Category:",
    options=data["age_category"].unique(),
    default=data["age_category"].unique()
)
# select month
month = st.sidebar.multiselect(
    "Select the Month:",
    options=data["month"].unique(),
    default=data["month"].unique()
)

data_selection = data.query(
    "Gender == @city & month == @month & age_category == @age_category"
)
st.dataframe(data_selection)

# Main page

st.title(":bar_chart: Online Store Sales Dashboard")
st.markdown("##")

# Top KPIs
Total_number_of_purchases = data_selection['N_Purchases'].sum()
Total_sales = round(data_selection['Purchase_VALUE'].sum(),2)
total_sales_by_male = data_selection[data_selection['Gender']==0]

males_sales = round(total_sales_by_male['Purchase_VALUE'].sum(),2)

total_sales_by_female = data_selection[data_selection['Gender']==1]

females_sales = round(total_sales_by_female['Purchase_VALUE'].sum(),2)


# Create columns for displaying KPIs horizontally
col1, col2, col3, col4 = st.columns(4)  

with col1:
    st.subheader("Total Number of Purchases:")
    st.subheader(Total_number_of_purchases)

with col2:
    st.subheader("Total Sales:")
    st.subheader(f"US ${Total_sales}")

with col3:
    st.subheader("Males Sales:")
    if not total_sales_by_male.empty:
        st.subheader(f"US ${males_sales}")
    else:
        st.subheader("No data for Males Sale")

with col4:
    st.subheader("Females Sales:")
    if not total_sales_by_female.empty:
        st.subheader(f"US ${females_sales}")
    else:
        st.subheader("No data for Females Sale")            


st.markdown("---")


age_data = data_selection.groupby(["age_category"])["Purchase_VALUE"].sum().reset_index().sort_values(by="Purchase_VALUE", ascending=False)


#st.markdown("##Sales by age ")
if not age_data.empty:
    fig = px.bar(
    age_data,
    x= "Purchase_VALUE",
    y= "age_category",
    orientation="h",
    title="Sales by age category",
    labels={"Purchase_VALUE": "Sales ($)", "age_category": "Age category"},
    color_discrete_sequence=["#0083B8"] * len(data_selection),
    )
else:
    st.warning("No data available for selected criteria.")    



#group data by month and age category

grouped_data = data_selection.groupby(["month", "Gender"])["Purchase_VALUE"].sum().reset_index()

if not grouped_data.empty:
   fig2 = px.line(
    grouped_data,
    x="month",
    y="Purchase_VALUE",
    color="Gender",
   title="Monthly trend of sales by Gender",
   labels={"month": "Month", "Purchase_VALUE": "sales ($)", "Gender": "Gender <br>0=Male <br>1=Female"},
)
else:
    st.warning("No data available for selected criteria.")   




# payment method analysis
if not data_selection.empty:
   fig3 = px.histogram(
    data_selection,
    x="purchase_value_category",
    color="Pay_Method",
    title="Customer count by Payment method for different<br> purchase amount ranges",
    labels={"purchase_value_category": "Purchase amount ($)",
            "Pay_Method": "Payment method <br>0=Digital Wallet <br>1=Card <br>2=Paypal <br>3=Other"},
    )
else:
    st.warning("No data available for selected criteria.")


# correlation between Time spent and purchase value category
if not data_selection.empty:
   fig4 = px.scatter(
    data_selection, x = "time_in_mins", y = "Purchase_VALUE", title= "Time Spent vs. Purchase Value", labels={"Purchase_VALUE": "Purchase Value ($)", "time_in_mins": "Time Spent (mins)"}
)
else:
    st.warning("No data available for selected criteria.") 

# realtion between purchase value category and news letter subscribed

fig5 = px.histogram(
    data_selection,
    x="purchase_value_category",
    color="Newsletter",
    title="Customer count by News Letter Subscription for different <br> purchase amount ranges",
    labels={"Purchase_VALUE": "Purchase amount ($)",
            "Newsletter": "News Letter Subscription <br>0=NO <br>1=YES "}
) 


# relation between purchase value category and voucher used
fig6 = px.histogram(
    data_selection,
    x="purchase_value_category",
    color="Voucher",
    title="Customer count by Voucher used for different <br> purchase amount ranges",
    labels={"purchase_value_category": "Purchase amount ($)",
            "Voucher": "Voucher used <br>0=NO <br>1=YES "}
)
monthly_sales = data_selection.groupby('month')['Purchase_VALUE'].sum().reset_index()
# pie chart
fig7 = px.line(
    monthly_sales,
    x='month',
    y='Purchase_VALUE',
    title='Monthly Sales'
)



browser_data = data_selection.groupby("Browser")["Customer_id"].count().reset_index()

fig8 = px.pie(
    browser_data,
    values="Customer_id",
    names="Browser",
    title="Browser Distribution",
    labels={"Customer_id": "Number of customers", "Browser": "Browser"},
    color_discrete_sequence=px.colors.sequential.Blues
)



leftcolumn, rightcolumn = st.columns(2)

leftcolumn.plotly_chart(fig7, use_container_width=True)
rightcolumn.plotly_chart(fig8, use_container_width=True)


leftcolumn, rightcolumn = st.columns(2)

leftcolumn.plotly_chart(fig, use_container_width=True)
rightcolumn.plotly_chart(fig2, use_container_width=True)



leftcolumn, rightcolumn = st.columns(2)
leftcolumn.plotly_chart(fig3, use_container_width=True)
rightcolumn.plotly_chart(fig4, use_container_width=True)


leftcolumn, rightcolumn = st.columns(2)
leftcolumn.plotly_chart(fig5, use_container_width=True)
rightcolumn.plotly_chart(fig6, use_container_width=True)


# To view the dashboard, run the following command in the terminal

streamlit run "streamlit run d:/my projects/segmentataion/myvenv/Scripts/dashboard.py"











