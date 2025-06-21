import streamlit as st
import pandas as pd

st.set_page_config(page_title="Market Basket Search", layout="centered")
st.title("🛍️ Market Basket Product Insights")

# Load CSVs
itemsets_df = pd.read_csv("frequent_itemsets_sample.csv.csv")
rules_df = pd.read_csv("association_rules_sample.csv.csv")

# 🧹 Clean columns (convert stringified lists to Python lists)
itemsets_df["items"] = itemsets_df["items"].apply(lambda x: [i.strip().lower() for i in x.split(",")])
rules_df["antecedent"] = rules_df["antecedent"].apply(lambda x: [i.strip().lower() for i in x.split(",")])
rules_df["consequent"] = rules_df["consequent"].apply(lambda x: [i.strip().lower() for i in x.split(",")])

# 🔍 User input
st.subheader("🔎 Search for a Product")
search_product = st.text_input("Enter a product name (e.g., milk, eggs, bread):").strip().lower()

if search_product:
    # 1️⃣ Frequency count from frequent itemsets
    match_freq = itemsets_df[itemsets_df["items"].apply(lambda x: search_product in x)]
    total_count = match_freq["freq"].sum()

    if total_count > 0:
        st.success(f"✅ '{search_product}' appeared in {int(total_count)} orders.")
    else:
        st.warning(f"❌ '{search_product}' not found in frequent itemsets.")

    # 2️⃣ Show matching association rules
    matching_rules = rules_df[rules_df["antecedent"].apply(lambda x: search_product in x)]

    if not matching_rules.empty:
        st.subheader("📦 Frequently Bought Together:")
        st.dataframe(matching_rules[["consequent", "confidence", "lift"]])
    else:
        st.info("No association rules found for this product.")
