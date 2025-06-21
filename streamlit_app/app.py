import streamlit as st
import pandas as pd

st.set_page_config(page_title="Market Basket Search", layout="centered")
st.title("🛒 Market Basket Analyzer")

# Load CSVs (ensure these are in the same folder)
itemsets_df = pd.read_csv("frequent_itemsets_sample.csv.csv")
rules_df = pd.read_csv("association_rules_sample.csv.csv")

# Convert stringified arrays to actual lists
itemsets_df["items"] = itemsets_df["items"].apply(lambda x: x.split(","))
rules_df["antecedent"] = rules_df["antecedent"].apply(lambda x: x.split(","))
rules_df["consequent"] = rules_df["consequent"].apply(lambda x: x.split(","))

# Product search input
st.subheader("🔍 Search for a product")
product = st.text_input("Enter a product name (e.g., milk, bread):").strip().lower()

if product:
    # 1. Frequency of the product
    count = itemsets_df[itemsets_df["items"].apply(
        lambda items: product in [i.strip().lower() for i in items]
    )]["freq"].sum()

    st.markdown(f"✅ **'{product}' was bought in {int(count)} orders**")

    # 2. Find associated products
    related = rules_df[rules_df["antecedent"].apply(
        lambda x: product in [i.strip().lower() for i in x]
    )]

    if not related.empty:
        st.subheader("🧾 Frequently bought together with it:")
        st.dataframe(related[["consequent", "confidence", "lift"]])
    else:
        st.warning("No strong association rules found for this product.")
