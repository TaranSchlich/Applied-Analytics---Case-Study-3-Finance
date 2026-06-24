# =====================================================================
# Urban Hamster Pricing Hub — Streamlit in Snowflake
# A product pricing tool for the sales team to use in vendor negotiations.
# Shows pricing, margins, and sales, filterable by department, category,
# and brand. Built on the `product_details` view.
# =====================================================================

# Import python packages
import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Initialize Snowflake session.
from snowflake.snowpark.context import get_active_session
session = get_active_session()

# Load the data into a Pandas data frame.
df_products = session.table("product_details").to_pandas()

# Naming application and detailing use case
st.title('Urban Hamster Pricing Hub')
st.write('Product pricing, margins, and sales to support vendor negotiations '
         'via filtering by department, category, and brand.')

# Sidebar subheader stating data filtering options
st.sidebar.subheader('Data Filtering Options')

# Create drop downs from a unique list sorted alphabetically (None-safe)
departments = sorted([d for d in df_products['Department'].unique().tolist() if d is not None])
categories  = sorted([c for c in df_products['Category'].unique().tolist()  if c is not None])
brands      = sorted([b for b in df_products['Brand'].unique().tolist()     if b is not None])

# Naming dropdowns and populating them with the sorted lists
selected_departments = st.sidebar.multiselect('Department', departments)
selected_categories  = st.sidebar.multiselect('Category', categories)
selected_brands      = st.sidebar.multiselect('Brand', brands)

# Apply filters. If no selection is made for a field, all products are shown.
filtered_df = df_products.copy()

if selected_departments:
    filtered_df = filtered_df[filtered_df['Department'].isin(selected_departments)]

if selected_categories:
    filtered_df = filtered_df[filtered_df['Category'].isin(selected_categories)]

if selected_brands:
    filtered_df = filtered_df[filtered_df['Brand'].isin(selected_brands)]

# -------------------- KPI metrics (react to filters) --------------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

product_count        = filtered_df['Product ID'].nunique()
total_sales_k        = filtered_df['Total Sales'].sum() / 1000
avg_product_sales_k  = filtered_df['Total Sales'].mean() / 1000
avg_profit_margin_pct = filtered_df['Product Profit Margin (%)'].mean()

with kpi1:
    st.metric(label='Products', value=f"{product_count:,}")
with kpi2:
    st.metric(label="Total Sales ($K)", value=f"{total_sales_k:,.1f}")
with kpi3:
    st.metric(label="Average Product Sales ($K)", value=f"{avg_product_sales_k:,.1f}")
with kpi4:
    st.metric(label="Average Profit Margin (%)", value=f"{avg_profit_margin_pct:.1f}%")

# -------------------- Visuals (react to filters) ------------------------
# Visual 1 — distribution of product prices
st.subheader("Distribution of Product Prices")
st.write("Shows how product retail prices are distributed across the selected products.")
fig1 = sns.displot(filtered_df, x="Retail Price", bins=30, kde=True)
fig1.set_axis_labels("Retail Price ($)", "Number of Products")
st.pyplot(fig1)

# Visual 2 — distribution of product profit margins (%)
st.subheader("Distribution of Product Profit Margins (%)")
st.write("Displays the spread of profit margins across products after applying filters.")
fig2 = sns.displot(filtered_df, x="Product Profit Margin (%)", bins=30, kde=True)
fig2.set_axis_labels("Product Profit Margin (%)", "Number of Products")
st.pyplot(fig2)

# Visual 3 — product count by category (alphabetized)
st.subheader("Product Count by Category")
st.write("Shows the number of products in each category after applying filters.")
category_counts = (
    filtered_df
    .groupby("Category")
    .size()
    .reset_index(name="Product Count")
    .sort_values("Category")
)
fig3, ax = plt.subplots()
sns.barplot(data=category_counts, x="Category", y="Product Count", ax=ax)
ax.set_xlabel("Category")
ax.set_ylabel("Number of Products")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig3)

# -------------------- Data table (filtered rows) ------------------------
st.subheader("Product Details Table")
st.write("All products matching the selected filters, with full pricing, margin, and sales detail.")
st.dataframe(filtered_df)
