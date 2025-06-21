import streamlit as st
import pandas as pd

st.set_page_config(page_title="Market Basket Search", layout="centered")
st.title("🛍️ Market Basket Product Insights")

# File upload section
st.sidebar.header("📂 Upload Your CSV Files")
itemsets_file = st.sidebar.file_uploader("Upload Frequent Itemsets CSV", type="csv")
rules_file = st.sidebar.file_uploader("Upload Association Rules CSV", type="csv")

# Only proceed if both files are uploaded
if itemsets_file and rules_file:
    # Load CSVs from upload
    itemsets_df = pd.read_csv(itemsets_file)
    rules_df = pd.read_csv(rules_file)

    # Clean and parse stringified lists
    itemsets_df["items"] = itemsets_df["items"].apply(lambda x: [i.strip().lower() for i in x.split(",")])
    rules_df["antecedent"] = rules_df["antecedent"].apply(lambda x: [i.strip().lower() for i in x.split(",")])
    rules_df["consequent"] = rules_df["consequent"].apply(lambda x: [i.strip().lower() for i in x.split(",")])

    # Input section
    st.subheader("🔎 Search for a Product")
    search_product = st.text_input("Enter a product name (e.g., milk, bread):").strip().lower()

    if search_product:
        # Frequency check
        match_freq = itemsets_df[itemsets_df["items"].apply(lambda x: search_product in x)]
        total_count = match_freq["freq"].sum()

        if total_count > 0:
            st.success(f"✅ '{search_product}' appeared in {int(total_count)} orders.")
        else:
            st.warning(f"❌ '{search_product}' not found in frequent itemsets.")

        # Associated products
        matching_rules = rules_df[rules_df["antecedent"].apply(lambda x: search_product in x)]

        if not matching_rules.empty:
            st.subheader("📦 Frequently Bought Together:")
            st.dataframe(matching_rules[["consequent", "confidence", "lift"]])
        else:
            st.info("No association rules found for this product.")
else:
    st.warning("⬅️ Please upload both CSV files in the sidebar to continue.")
